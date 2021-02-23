# For more mostly useless soykaf, please consider going to:
# http://jarlold.netai.net
# I'll make a Discord bot or something for you if you pay me.
# -Jarlold

from scapy.all import *
from datetime import datetime
from threading import Thread
from time import sleep
from sys import stdout
from sys import argv


help_advice = """
WifiSharingan, a program to detect nearby 802.11 probes, so no ninja sneak up on you.
Usage: wifi_sharingan [iface] [verbose (true|false)]
[!] Remember to put your wifi card into monitor mode (use airmon-ng start [iface] or
    iwconfig if you're a massochist I guess)
"""

# Parse the command line arguments.
if len(argv) < 2 or "--help" in argv or "-help" in argv: # check for help
    print(help_advice)

wifi_dev = str(argv[1]) # get the wifi device
verbose_mode = True if len(argv) >= 3 and str(argv[2]) == "true" else False # check for verbose


# A record of the packets from the last 50 seconds, will be used to determine when a device
# has left.
global last_x_packets
last_x_packets = list()

# List to hold the devices within broadcasting range that we've heard from recently.
nearby_devices = list()

# We want to log which MAC address have sent out beacon-only packets so we can ignore them
beacon_addresses = []

# Prints out the "device joined" notice
def new_device_nearby(addr, sig_stren):
    hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
    print("DEVICE --> : [{}:{}:{}] : {} : {}".format(hour, minute, second, addr, sig_stren))

# Prints out the "device left" notice
def new_device_left(addr):
    hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
    print("DEVICE <-- : [{}:{}:{}] : {}".format(hour, minute, second, addr))


# Every 50 seconds, remove any nearby devices that we haven't heard from.
def clear_missing_devices():
    global last_x_packets
    while True:
        sleep(50)
        for i in nearby_devices: # If the device is in nearby dev but not the recent packets, remove it
            if not i in last_x_packets:
                nearby_devices.remove(i)
                new_device_left(i)

        if verbose_mode: # If we're in verbose mode, print out which devices are in the recent packets
           print("last x packets:")
           for i in last_x_packets:
               print("  --> " + i)

           print("nearby devices:") # as well as which devices are considered "nearby"
           for i in nearby_devices:
               print("  --> " + i)

        last_x_packets = list() # Reset the recent packets log.

# Runs when scapy finds a packet
def scan_callback(pack):

    # Check if the packet is type management, subtype beacon
    if pack.getlayer(Dot11).subtype == 8 and pack.getlayer(Dot11).type == 0:
        # Record beacon frame sender addresses since they're probably beacons.
        if not pack.getlayer(Dot11).addr2.upper() in beacon_addresses:
            beacon_addresses.append(pack.getlayer(Dot11).addr2.upper())

            if verbose_mode:
                print("BEACON " + pack.getlayer(Dot11).addr2.upper())

        # Make sure there are no beacons in the last_x_packets
        if pack.getlayer(Dot11).addr2.upper() in last_x_packets:
            last_x_packets.remove(pack.getlayer(Dot11).addr2.upper())
            

    # Checks if the packet is type management, subtype probe request
    #if pack.getlayer(Dot11).subtype == 4 and pack.getlayer(Dot11).type == 0:

    # If a packet with a sender address is recieved, and it's not in the beacons list, and it's not
    # a beacon frame, then we can parse it.
    if (
        pack.getlayer(Dot11).addr2 is not None
        and pack.getlayer(Dot11).addr2.upper() not in beacon_addresses
        and not (pack.getlayer(Dot11).subtype == 8 and pack.getlayer(Dot11).type == 0)
        ):

        sig_stren = pack[scapy.layers.dot11.RadioTap].dBm_AntSignal
        og_addr = pack.getlayer(Dot11).addr2.upper() 
        addr2 = pack.getlayer(Dot11).addr2.upper()[:8] # The manufactuerer seems to stay the same
                                                       # and they randomize the last part.

        # Add it to the packet log!
        last_x_packets.append(addr2)
    
        # Ignore far away ninjas
        if sig_stren < -50:
            return

        # If we're in verbose mode, print packets even if the device isn't new to the scene
        #if verbose_mode:
        #        new_device_nearby(og_addr, sig_stren)

        # When we're not in verbose mode, look for devices that aren't nearby, and notify the user
        # of their arrival
        if not verbose_mode:
            if not addr2 in nearby_devices:
                nearby_devices.append(addr2)
                new_device_nearby(addr2, sig_stren)


if __name__ == "__main__":
    print("Starting scan...")

    # Make a thread to clear out the old packets
    packet_clear_thread = Thread(target=clear_missing_devices)
    packet_clear_thread.daemon = True
    packet_clear_thread.start()

    # Start the 802.11 sniffing
    sniff(prn=scan_callback, iface=wifi_dev)

