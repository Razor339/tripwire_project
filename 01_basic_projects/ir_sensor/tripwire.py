#!/usr/bin/env python3
"""
🚦 IR BREAK-BEAM TRIPWIRE
When the invisible beam is broken, print an alert!

Beginner-friendly version using Raspberry Pi GPIO.
"""

import RPi.GPIO as GPIO
import time

print("🚀 Tripwire starting up...")
print("Tip: Point the transmitter straight at the receiver.")

# Use BCM numbering (GPIO17 means the pin labeled 17 in code charts)
GPIO.setmode(GPIO.BCM)

# Choose which pin the receiver OUT is connected to
SENSOR_PIN = 17  # GPIO17 (physical pin 11)

# Set up the pin as an INPUT with an internal PULL-UP resistor
# This keeps the value HIGH unless the sensor pulls it LOW
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# We'll count how many times the beam is broken
beam_break_count = 0

# This function runs when the beam is broken (input goes from HIGH to LOW)
def on_beam_broken(channel: int) -> None:
    global beam_break_count
    beam_break_count += 1
    print("\n🚨 INTRUDER! Beam broken! (#{} times)".format(beam_break_count))

# This function runs when the beam is restored (input goes from LOW to HIGH)
def on_beam_restored(channel: int) -> None:
    print("✅ Beam restored. All clear.")

# Add event detection: falling edge = HIGH -> LOW (beam broken)
GPIO.add_event_detect(SENSOR_PIN, GPIO.FALLING, callback=on_beam_broken, bouncetime=200)
# Rising edge = LOW -> HIGH (beam restored)
GPIO.add_event_detect(SENSOR_PIN, GPIO.RISING, callback=on_beam_restored, bouncetime=200)

try:
    print("\nReady! Break the beam to trigger the alarm.")
    # Keep the program running forever (until Ctrl+C)
    while True:
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n🛑 Stopping tripwire. Goodbye!")
finally:
    GPIO.cleanup()
    print("✅ GPIO cleaned up.")


