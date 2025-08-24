#!/usr/bin/env python3
"""
🔴 LASER BLINK PROJECT 🔴
A simple program to make a laser pointer blink on and off!

This is your first step into controlling real-world devices with code!
We're going to make a laser turn on for 1 second, off for 1 second, and repeat.

Author: Your Awesome Tutor 😄
For: The Future Engineer (that's you!)
Safety: NEVER look directly at the laser beam!
"""

# STEP 1: Import the libraries we need
# Think of libraries like toolboxes - they contain tools (functions) we can use!

import RPi.GPIO as GPIO  # This toolbox lets us control the Pi's pins
import time             # This toolbox lets us work with time (like waiting)

print("🚀 Starting Laser Blink Project!")
print("⚠️  Remember: NEVER look directly at the laser!")
print("💡 The laser will blink every second...")

# STEP 2: Set up how we want to talk to the GPIO pins
# BCM means we use the GPIO numbers (like GPIO18) instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# STEP 3: Choose which pin our laser is connected to
# We connected our laser to GPIO pin 18 (that's physical pin 12 on the Pi)
LASER_PIN = 18

# STEP 4: Tell the Pi this pin should send electricity OUT (not receive it)
# Think of it like setting a water faucet to "flow out" instead of "suck in"
GPIO.setup(LASER_PIN, GPIO.OUT)

# STEP 5: Start our blinking loop!
try:
    # This creates an infinite loop - it will keep going until we stop it
    while True:
        
        # Turn the laser ON
        # GPIO.HIGH means "send electricity" (like turning on a light switch)
        GPIO.output(LASER_PIN, GPIO.HIGH)
        print("🔴 Laser ON!")  # Tell us what's happening
        
        # Wait for 1 second while the laser is on
        # time.sleep(1) means "do nothing for 1 second"
        time.sleep(1)
        
        # Turn the laser OFF  
        # GPIO.LOW means "stop sending electricity" (like turning off a light switch)
        GPIO.output(LASER_PIN, GPIO.LOW)
        print("⚫ Laser OFF!")  # Tell us what's happening
        
        # Wait for 1 second while the laser is off
        time.sleep(1)
        
        # The loop will now go back to the top and repeat!
        # This creates our blinking pattern: ON-OFF-ON-OFF-ON-OFF...

# STEP 6: Handle when someone wants to stop the program
except KeyboardInterrupt:
    # This happens when someone presses Ctrl+C
    print("\n🛑 Someone pressed Ctrl+C - stopping the laser!")
    
# STEP 7: Clean up when we're done
finally:
    # This is VERY important! We need to tell the Pi we're done using the pins
    # It's like putting away your toys when you're finished playing
    GPIO.cleanup()
    print("✅ All cleaned up! Thanks for using the Laser Blink project!")
    print("🎉 You just controlled a real device with code - you're amazing!")

"""
🤔 UNDERSTANDING THE CODE:

1. IMPORTS: We bring in tools (libraries) we need
2. SETUP: We tell the Pi how we want to use the pins  
3. CONFIGURATION: We choose which pin and set it as output
4. MAIN LOOP: We repeatedly turn the laser on and off
5. ERROR HANDLING: We handle when someone wants to stop
6. CLEANUP: We properly shut down and clean up

🎯 KEY CONCEPTS:
- GPIO pins can be INPUT (receive signals) or OUTPUT (send signals)
- GPIO.HIGH = electricity flowing = device ON
- GPIO.LOW = no electricity = device OFF
- time.sleep() makes the program wait
- try/except helps handle errors gracefully
- GPIO.cleanup() is important to reset everything

🚀 NEXT CHALLENGES:
- Can you make it blink faster? (Change the time.sleep values!)
- Can you make it blink in a pattern? (Different on/off times!)
- Can you add more print statements to make it more fun?
"""
