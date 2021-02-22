# Wifi Sharingan 
<p align="center">
  <img src="./sharingan.gif"/>
</p>

So in Naruto ninja can detect eachothers presence through their ninja senses, and they can have special
eye-characteristics (such as sharingan) that allow them to detect more through ninja magic.<br><br>

I thought this was super cool, but according to Wikipedia ninja magic isn't real- so I had to improvise. <br>


## What does it do though?
It tracks 802.11 beacon packets (which are sent out by wifi devices to detect available networks) and can be
used to trigger an alert when someone is nearby. So that no ninja can sneak up on you. This is pretty useless
other than making me feel really cool.

## How do I install it?
There's no python environment because I am lazy, so do the following instead: <br><br>
```
+ Clone the repo into some folder
+ Install the following python packages
+ Install airmon-ng (from the aircrack suite)
+ Set your wifi card to monitor mode
+ Run the script
```

<br>

If you want to do something fun, try using `entr` or a similar program to set off a notification when people
get too close to you.

