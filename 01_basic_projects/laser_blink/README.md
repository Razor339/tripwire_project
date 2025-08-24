# 🔴 Project 1: Laser Blink
*Your first laser project - making it turn on and off!*

## 🎯 What This Project Does

This project teaches you how to control a laser pointer with your Raspberry Pi! The laser will:
- Turn ON for 1 second
- Turn OFF for 1 second  
- Repeat forever (until you stop the program)

Think of it like a lighthouse - blinking to send signals! 🚢

## 🧠 What You'll Learn

- How to connect a laser to your Pi safely
- How to write Python code that controls real devices
- How to use GPIO pins (the special connectors on your Pi)
- How to make your program wait and repeat actions

## 🔌 What You Need

- Raspberry Pi 5
- Laser diode module (3.3V or 5V)
- 2 jumper wires (male-to-female)
- Breadboard (optional, but recommended for learning)

## ⚠️ SAFETY REMINDER

**NEVER look directly into the laser beam!** Point it at a wall or piece of paper, never at people, animals, or mirrors!

## 🔧 Wiring Instructions

```
Raspberry Pi Pin → Laser Module Pin
GPIO 18 (Pin 12) → Signal/Data Pin (usually marked + or S)
Ground (Pin 6)   → Ground Pin (usually marked - or GND)
```

**Visual Guide:**
```
Pi Pin Layout:
 1  2
 3  4
 5  6  ← Ground (connect to laser -)
 7  8
 9 10
11 12  ← GPIO 18 (connect to laser +)
...
```

## 🐍 The Code Explained

Open `laser_blink.py` and let's understand every line:

```python
# This imports the GPIO library - it lets us control the Pi's pins
import RPi.GPIO as GPIO
# This imports time - it lets us make the program wait
import time

# This tells the Pi how we want to number the pins
GPIO.setmode(GPIO.BCM)

# This is the pin number we connected our laser to
LASER_PIN = 18

# This tells the Pi that pin 18 should send electricity OUT (not receive it in)
GPIO.setup(LASER_PIN, GPIO.OUT)
```

## 🚀 How to Run

1. **Connect your laser** following the wiring diagram above
2. **Open terminal** on your Pi
3. **Navigate to this folder:**
   ```bash
   cd ~/pi-sensor-projects/01_basic_projects/laser_blink
   ```
4. **Run the program:**
   ```bash
   python3 laser_blink.py
   ```
5. **Watch your laser blink!** ✨
6. **To stop:** Press `Ctrl + C`

## 🔍 Troubleshooting

**Laser doesn't turn on?**
- Check your wires are connected firmly
- Make sure the laser module isn't broken (try connecting it directly to 3.3V)
- Verify you're using the right pin numbers

**Getting error messages?**
- Make sure you ran `sudo raspi-config` to enable GPIO
- Check that you installed the GPIO library: `pip3 install RPi.GPIO`

**Program won't stop?**
- Press `Ctrl + C` firmly
- If that doesn't work, close the terminal window

## 🎮 Fun Experiments to Try

Once you get the basic blinking working, try these modifications:

1. **Change the speed:** Make it blink faster or slower
2. **Morse code:** Make it spell out "SOS" (short-short-short, long-long-long, short-short-short)
3. **Pattern:** Create a custom blinking pattern
4. **Multiple lasers:** Connect more lasers to different pins!

## 🤔 Questions to Think About

- Why do we need to tell the Pi that the pin is an OUTPUT?
- What would happen if we used GPIO.IN instead?
- How could we make the laser stay on for different amounts of time?
- Could you make it blink in a pattern that means something?

## ⭐ What's Next?

Great job! You've just controlled your first real-world device with code! 🎉

Next up: **Light Sensor Project** - teaching your Pi to "see" brightness levels!

---
*Remember: Every expert was once a beginner. You're doing great! 💪*
