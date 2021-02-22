# WiFi Sharingan 
<p align="center">
  <img src="./sharingan.gif"/>
</p>

So in Naruto ninja can detect eachother's presence through their ninja senses, and they can have special
eye-characteristics (such as sharingan) that allow them to detect more through ninja magic.<br><br>

I thought this was super cool, but according to Wikipedia ninja magic isn't real- so I had to improvise. <br>


## What does it do though?
It tracks 802.11 probe request packets (which are sent out by WiFi devices to detect available networks) and can be
used to trigger an alert when someone is nearby. This way if some world class shinobi tries to get the jump on you,
the probe packets his smartphone is sending out will give him away.

## More detail on how it works
### How it actually works
Right now the script is only set to monitor the probe request packets. I intend to change this so that
dataframes and other shenanigans are picked up as well, but I'm a busy boi. You might have heard somewhere
that the mac addresses used in WiFi packets send from Android and Apple devices are randomized, and
that's mostly-true, however due to regulation, manufacturers can't broadcast with the MAC address of another
company, so devices are tracked by the first few hex characters of their address.<br><br>

While this data might not be good enough for commercial tracking (such as trade-shows or supermarkets) it's
good enough to detect the presence of other people- which makes it cool but useless.

Some fun changes to make in the future would be:<br>
```
+ Since these packets are sent out in certain intervals, you could determine the number of people more
accurately by the frequency of a mac address being sent out.
+ If you got two antenna you could track the locations of people (roughly) based off the signal strength.
+ You could wire this to a smart watch with a "number of people" counter on it.
```

### How I wished it worked
For most WiFi devices, once they connect to a network they start using their actual MAC address. So
theoretically if you pretended your SSID was `AT&T WiFi` or `Starbuck's Wifi` you could get a bunch of devices
to connect, and then manage them more specifically!

<p align="center">
  <img src="./wait_thats_illegal.jpeg"/>
</p>

It would also mean that you can be tracked fairly easily, just by looking for the man walking around broadcasting
every known SSID on the planet. And would be super battery intensive. 


## Installation
### Linux Installation
There's no python environment because I am lazy, so do the following instead: <br><br>
```
+ Clone the repo into some folder
+ Install the following python packages:
    + scapy
+ Install airmon-ng (from the aircrack suite)
+ Set your WiFi card to monitor mode
+ Run the script
```

If you want to do something fun, try using `entr` or a similar program to set off a notification when people
get too close to you.

### Windows Installation
*(distant laughter)*

## Usage
to use the script run `python ./wifi_sharingan.py [MONITOR MODE WIFI DEVICE] [VERBOSE]` <br>


