#!/usr/bin/env python3
"""
🎯 LIGHT-FOLLOWING LASER PROJECT
An intermediate project that tracks light sources and points a laser toward them!

This project uses:
- Two photoresistors (LDR) to detect light direction
- Two servo motors to control laser position (X and Y axis)
- A laser pointer module

How it works:
1. Read light levels from two sensors positioned at different angles
2. Compare readings to determine which direction has more light
3. Move servos to point laser toward the brighter area
4. Continuously adjust position to track moving light sources

Author: AI Tutor
Safety: NEVER look directly at the laser beam!
"""

import time
import math
from typing import Tuple

import RPi.GPIO as GPIO

print("🚀 Starting Light-Following Laser Project!")
print("⚠️  SAFETY: Never look directly at the laser!")
print("💡 Point a flashlight around to see the laser follow it...")

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Pin Configuration
LASER_PIN = 18          # Laser pointer control
SERVO_X_PIN = 12        # Horizontal servo (PWM pin)
SERVO_Y_PIN = 13        # Vertical servo (PWM pin)  
LDR_LEFT_PIN = 21       # Left light sensor
LDR_RIGHT_PIN = 20      # Right light sensor
LDR_UP_PIN = 16         # Up light sensor
LDR_DOWN_PIN = 19       # Down light sensor

# Setup pins
GPIO.setup(LASER_PIN, GPIO.OUT)
GPIO.setup(SERVO_X_PIN, GPIO.OUT)
GPIO.setup(SERVO_Y_PIN, GPIO.OUT)
GPIO.setup(LDR_LEFT_PIN, GPIO.OUT)
GPIO.setup(LDR_RIGHT_PIN, GPIO.OUT)
GPIO.setup(LDR_UP_PIN, GPIO.OUT)
GPIO.setup(LDR_DOWN_PIN, GPIO.OUT)

# Create PWM instances for servos (50Hz is standard for servos)
servo_x = GPIO.PWM(SERVO_X_PIN, 50)
servo_y = GPIO.PWM(SERVO_Y_PIN, 50)

# Start PWM with neutral position (7.5% duty cycle = 90 degrees)
servo_x.start(7.5)
servo_y.start(7.5)

# Turn on laser
GPIO.output(LASER_PIN, GPIO.HIGH)

# Current servo positions (in degrees, 0-180)
current_x = 90
current_y = 90

def discharge_capacitor(pin: int) -> None:
    """Discharge the RC timing capacitor for LDR reading."""
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.005)  # 5ms discharge time

def read_ldr_time(pin: int, timeout: float = 0.1) -> float:
    """
    Read LDR using RC timing method.
    Returns charge time in milliseconds.
    Lower time = brighter light, higher time = darker.
    """
    discharge_capacitor(pin)
    GPIO.setup(pin, GPIO.IN)
    
    start_time = time.perf_counter()
    deadline = start_time + timeout
    
    while time.perf_counter() < deadline:
        if GPIO.input(pin) == GPIO.HIGH:
            elapsed = (time.perf_counter() - start_time) * 1000
            return elapsed
    
    # Timeout reached (very dark)
    return timeout * 1000

def get_light_readings() -> Tuple[float, float, float, float]:
    """Get readings from all four LDR sensors."""
    left = read_ldr_time(LDR_LEFT_PIN)
    right = read_ldr_time(LDR_RIGHT_PIN)
    up = read_ldr_time(LDR_UP_PIN)
    down = read_ldr_time(LDR_DOWN_PIN)
    
    return left, right, up, down

def degrees_to_duty_cycle(degrees: float) -> float:
    """
    Convert servo angle (0-180 degrees) to PWM duty cycle.
    0° = 2.5% duty cycle (0.5ms pulse)
    90° = 7.5% duty cycle (1.5ms pulse)  
    180° = 12.5% duty cycle (2.5ms pulse)
    """
    # Clamp degrees to valid range
    degrees = max(0, min(180, degrees))
    
    # Convert to duty cycle percentage
    duty_cycle = 2.5 + (degrees / 180.0) * 10.0
    return duty_cycle

def move_servo(servo, current_pos: float, target_pos: float, max_step: float = 2.0) -> float:
    """
    Smoothly move servo toward target position.
    Returns the new current position.
    """
    # Calculate direction and step size
    diff = target_pos - current_pos
    
    if abs(diff) <= max_step:
        # Close enough, move directly to target
        new_pos = target_pos
    else:
        # Move one step toward target
        step = max_step if diff > 0 else -max_step
        new_pos = current_pos + step
    
    # Clamp to servo limits
    new_pos = max(30, min(150, new_pos))  # Keep servos away from extreme positions
    
    # Set servo position
    duty_cycle = degrees_to_duty_cycle(new_pos)
    servo.ChangeDutyCycle(duty_cycle)
    
    return new_pos

def calculate_target_position(left: float, right: float, up: float, down: float) -> Tuple[float, float]:
    """
    Calculate target servo positions based on light sensor readings.
    Remember: lower reading = brighter light
    """
    # Calculate horizontal target (X-axis)
    # If left sensor has lower reading (brighter), move left (decrease angle)
    # If right sensor has lower reading (brighter), move right (increase angle)
    horizontal_diff = left - right  # Positive means right is brighter
    
    # Calculate vertical target (Y-axis)  
    # If up sensor has lower reading (brighter), move up (decrease angle)
    # If down sensor has lower reading (brighter), move down (increase angle)
    vertical_diff = up - down  # Positive means down is brighter
    
    # Scale the differences to servo movement
    # Larger differences in light levels = more aggressive movement
    sensitivity = 0.5  # Adjust this to make following more/less aggressive
    
    target_x = current_x + (horizontal_diff * sensitivity)
    target_y = current_y + (vertical_diff * sensitivity)
    
    return target_x, target_y

def print_status(left: float, right: float, up: float, down: float, x: float, y: float) -> None:
    """Print current sensor readings and servo positions."""
    print(f"Light: L={left:4.1f} R={right:4.1f} U={up:4.1f} D={down:4.1f} | Servo: X={x:5.1f}° Y={y:5.1f}°")

try:
    print("\n🎯 Light follower is active!")
    print("💡 Shine a flashlight around to see the laser follow it")
    print("🔧 Tip: Start with the light source in front of the sensors")
    
    time.sleep(1)  # Let servos reach initial position
    
    while True:
        # Read all light sensors
        left, right, up, down = get_light_readings()
        
        # Calculate where we should point
        target_x, target_y = calculate_target_position(left, right, up, down)
        
        # Smoothly move servos toward target
        current_x = move_servo(servo_x, current_x, target_x)
        current_y = move_servo(servo_y, current_y, target_y)
        
        # Print status for debugging
        print_status(left, right, up, down, current_x, current_y)
        
        # Small delay for smooth operation
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\n🛑 Stopping light follower...")

finally:
    # Clean shutdown
    print("🔧 Moving servos to center position...")
    servo_x.ChangeDutyCycle(7.5)  # Center position
    servo_y.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    
    # Stop PWM and turn off laser
    servo_x.stop()
    servo_y.stop()
    GPIO.output(LASER_PIN, GPIO.LOW)
    
    # Clean up GPIO
    GPIO.cleanup()
    print("✅ All cleaned up!")
    print("🎉 Thanks for playing with the light follower!")

"""
🤔 HOW THIS WORKS:

1. SENSOR SETUP: Four LDR sensors positioned around the laser mount
   - Left/Right sensors detect horizontal light direction
   - Up/Down sensors detect vertical light direction

2. RC TIMING: Each LDR uses a capacitor for timing-based readings
   - Bright light = low resistance = fast charge = small time value
   - Dim light = high resistance = slow charge = large time value

3. SERVO CONTROL: Two servos control laser direction
   - X-axis servo: horizontal movement (left/right)
   - Y-axis servo: vertical movement (up/down)

4. TRACKING ALGORITHM:
   - Compare left vs right sensor readings
   - Compare up vs down sensor readings  
   - Move servos toward brighter direction
   - Smooth movement prevents jittery tracking

🎯 TUNING TIPS:
- Adjust 'sensitivity' to make tracking more/less aggressive
- Adjust 'max_step' to make movement smoother/faster
- Position sensors at different angles for better directional sensing
- Use diffusers on sensors to prevent direct laser feedback

🚀 ENHANCEMENT IDEAS:
- Add LED status indicators
- Implement automatic calibration
- Add multiple light source tracking
- Create preset positions and patterns
"""


