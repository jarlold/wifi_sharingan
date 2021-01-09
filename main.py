from scapy.all import *
from datetime import datetime
from threading import Thread
from time import sleep
from sys import stdout
from sys import argv

import bluetooth_server

# Identify clients trying to authenticate
# Identify authenticated clients
# Identify client advertisments

help_advice = """
WifiSharingan, a program to detect nearby 802.11 probes, so no ninja sneak up on you.
Usage: wifi_sharingan [iface] [verbose (true|false)]
[!] Remember to put your wifi card into monitor mode (use airmon-ng start [iface] or
    iwconfig if you're a massochist I guess)
"""

if len(argv) < 2:
    print(help_advice)

wifi_dev = str(argv[1])
verbose_mode = True if len(argv) >= 3 and str(argv[2]) == "true" else False

nearby_devices = list()

# List of Access Points MAC address, so we can filter them out and only find clients
APs = []

global last_x_packets
last_x_packets = list()

def new_device_nearby(addr, sig_stren):
    hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
    print("DEVICE --> : [{}:{}:{}] : {} : {}".format(hour, minute, second, addr, sig_stren))

def new_device_left(addr):
    hour, minute, second = datetime.now().hour, datetime.now().minute, datetime.now().second
    print("DEVICE <-- : [{}:{}:{}] : {}".format(hour, minute, second, addr))

def clear_missing_devices():
    global last_x_packets
    while True:
        sleep(50)
        for i in nearby_devices:
            if not i in last_x_packets:
                nearby_devices.remove(i)
                new_device_left(i)

#       if verbose_mode:
#           print("last x packets:")
#           for i in last_x_packets:
#               print("  --> " + i)

#           print("nearby devices:")
#           for i in nearby_devices:
#               print("  --> " + i)

        last_x_packets = list()

def scan_callback(pack):
#   if pkt.haslayer(Dot11Beacon):
#       bss = pkt.getlayer(Dot11).addr2.upper()
#       if bss not in APs:
#           APs.append(bss)

    #if pack.getlayer(Dot11).subtype == 4 and pack.getlayer(Dot11).type == 0:
    if pack.getlayer(Dot11).type == 0 and not pack.haslayer(Dot11Beacon):
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
        if verbose_mode:
                new_device_nearby(og_addr, sig_stren)

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


    # Make a thread to respond to the bluetooth connection
#   bluetooth_thread = Thread(target=bluetooth_server.main)
#   bluetooth_thread.daemon = True
#   bluetooth_thread.start()

