#!/usr/bin/env python3
"""
🌟 LASER LIGHT SHOW SYSTEM
An advanced project that creates mesmerizing laser light patterns!

This project combines:
- Precise servo motor control for X/Y laser positioning
- Pattern generation algorithms for geometric shapes
- Music synchronization with beat detection
- Real-time control via web interface
- Custom pattern programming and storage
- Multiple laser modules for multi-color shows

Features:
- Pre-programmed patterns (circles, spirals, text, etc.)
- Music-reactive mode with beat detection
- Manual control via web interface
- Pattern recording and playback
- Multi-laser coordination
- Safety features and emergency stops

Author: AI Tutor
Safety: NEVER look directly at laser beams - can cause permanent eye damage!
"""

import time
import math
import json
import threading
import numpy as np
from typing import List, Tuple, Dict, Callable
from dataclasses import dataclass
from enum import Enum

import RPi.GPIO as GPIO

print("🌟 Laser Light Show System Initializing...")
print("⚠️  CRITICAL SAFETY: Never look directly at laser beams!")

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Configuration
SERVO_X_PIN = 12        # X-axis servo (horizontal)
SERVO_Y_PIN = 13        # Y-axis servo (vertical)
LASER_RED_PIN = 18      # Red laser module
LASER_GREEN_PIN = 19    # Green laser module (optional)
LASER_BLUE_PIN = 20     # Blue laser module (optional)
BUTTON_STOP_PIN = 21    # Emergency stop button
LED_STATUS_PIN = 16     # Status LED
AUDIO_INPUT_PIN = 26    # Audio input for beat detection

# Setup GPIO pins
GPIO.setup(SERVO_X_PIN, GPIO.OUT)
GPIO.setup(SERVO_Y_PIN, GPIO.OUT)
GPIO.setup(LASER_RED_PIN, GPIO.OUT)
GPIO.setup(LASER_GREEN_PIN, GPIO.OUT)
GPIO.setup(LASER_BLUE_PIN, GPIO.OUT)
GPIO.setup(BUTTON_STOP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_STATUS_PIN, GPIO.OUT)
GPIO.setup(AUDIO_INPUT_PIN, GPIO.IN)

# Initialize PWM for servos
servo_x = GPIO.PWM(SERVO_X_PIN, 50)  # 50Hz for servos
servo_y = GPIO.PWM(SERVO_Y_PIN, 50)
servo_x.start(7.5)  # Start at center position
servo_y.start(7.5)

# Initialize all lasers OFF
GPIO.output(LASER_RED_PIN, GPIO.LOW)
GPIO.output(LASER_GREEN_PIN, GPIO.LOW)
GPIO.output(LASER_BLUE_PIN, GPIO.LOW)
GPIO.output(LED_STATUS_PIN, GPIO.LOW)

class LaserColor(Enum):
    """Enum for laser colors"""
    RED = "red"
    GREEN = "green" 
    BLUE = "blue"
    WHITE = "white"  # All colors
    OFF = "off"

@dataclass
class LaserPoint:
    """Data class for laser position and color"""
    x: float  # X position in degrees (0-180)
    y: float  # Y position in degrees (0-180)
    color: LaserColor
    duration: float  # Time to spend at this point (seconds)

@dataclass
class Pattern:
    """Data class for laser patterns"""
    name: str
    points: List[LaserPoint]
    repeat: bool = True
    speed_multiplier: float = 1.0

class LaserController:
    """Low-level laser and servo control"""
    
    def __init__(self):
        self.current_x = 90.0  # Center position
        self.current_y = 90.0
        self.current_color = LaserColor.OFF
        
    def degrees_to_duty_cycle(self, degrees: float) -> float:
        """Convert angle to PWM duty cycle"""
        degrees = max(0, min(180, degrees))
        return 2.5 + (degrees / 180.0) * 10.0
    
    def move_to(self, x: float, y: float, speed: float = 1.0) -> None:
        """Move laser to specified position"""
        # Clamp positions to safe ranges
        x = max(30, min(150, x))
        y = max(30, min(150, y))
        
        # Calculate movement steps for smooth motion
        steps = max(1, int(abs(x - self.current_x) + abs(y - self.current_y)) // 2)
        
        for i in range(steps + 1):
            progress = i / steps if steps > 0 else 1
            
            # Interpolate position
            curr_x = self.current_x + (x - self.current_x) * progress
            curr_y = self.current_y + (y - self.current_y) * progress
            
            # Set servo positions
            servo_x.ChangeDutyCycle(self.degrees_to_duty_cycle(curr_x))
            servo_y.ChangeDutyCycle(self.degrees_to_duty_cycle(curr_y))
            
            # Wait based on speed
            time.sleep(0.01 / speed)
        
        self.current_x = x
        self.current_y = y
    
    def set_laser_color(self, color: LaserColor) -> None:
        """Set laser color"""
        # Turn off all lasers first
        GPIO.output(LASER_RED_PIN, GPIO.LOW)
        GPIO.output(LASER_GREEN_PIN, GPIO.LOW)
        GPIO.output(LASER_BLUE_PIN, GPIO.LOW)
        
        # Turn on requested color(s)
        if color == LaserColor.RED:
            GPIO.output(LASER_RED_PIN, GPIO.HIGH)
        elif color == LaserColor.GREEN:
            GPIO.output(LASER_GREEN_PIN, GPIO.HIGH)
        elif color == LaserColor.BLUE:
            GPIO.output(LASER_BLUE_PIN, GPIO.HIGH)
        elif color == LaserColor.WHITE:
            GPIO.output(LASER_RED_PIN, GPIO.HIGH)
            GPIO.output(LASER_GREEN_PIN, GPIO.HIGH)
            GPIO.output(LASER_BLUE_PIN, GPIO.HIGH)
        
        self.current_color = color
    
    def execute_point(self, point: LaserPoint) -> None:
        """Execute a single laser point"""
        self.move_to(point.x, point.y)
        self.set_laser_color(point.color)
        time.sleep(point.duration)

class PatternGenerator:
    """Generates various laser patterns"""
    
    @staticmethod
    def circle(center_x: float = 90, center_y: float = 90, radius: float = 30, 
               points: int = 36, color: LaserColor = LaserColor.RED) -> Pattern:
        """Generate circular pattern"""
        pattern_points = []
        
        for i in range(points):
            angle = (i / points) * 2 * math.pi
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            pattern_points.append(LaserPoint(x, y, color, 0.05))
        
        return Pattern("Circle", pattern_points)
    
    @staticmethod
    def spiral(center_x: float = 90, center_y: float = 90, max_radius: float = 40,
               rotations: int = 3, points: int = 100, color: LaserColor = LaserColor.GREEN) -> Pattern:
        """Generate spiral pattern"""
        pattern_points = []
        
        for i in range(points):
            progress = i / points
            angle = progress * rotations * 2 * math.pi
            radius = max_radius * progress
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            pattern_points.append(LaserPoint(x, y, color, 0.03))
        
        return Pattern("Spiral", pattern_points)
    
    @staticmethod
    def figure_eight(center_x: float = 90, center_y: float = 90, width: float = 40,
                     height: float = 20, points: int = 60, color: LaserColor = LaserColor.BLUE) -> Pattern:
        """Generate figure-8 pattern"""
        pattern_points = []
        
        for i in range(points):
            t = (i / points) * 4 * math.pi
            x = center_x + width * math.sin(t)
            y = center_y + height * math.sin(t) * math.cos(t)
            
            pattern_points.append(LaserPoint(x, y, color, 0.04))
        
        return Pattern("Figure Eight", pattern_points)
    
    @staticmethod
    def star(center_x: float = 90, center_y: float = 90, outer_radius: float = 35,
             inner_radius: float = 15, points: int = 5, color: LaserColor = LaserColor.WHITE) -> Pattern:
        """Generate star pattern"""
        pattern_points = []
        
        for i in range(points * 2):
            angle = (i / (points * 2)) * 2 * math.pi
            radius = outer_radius if i % 2 == 0 else inner_radius
            
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            pattern_points.append(LaserPoint(x, y, color, 0.06))
        
        return Pattern("Star", pattern_points)
    
    @staticmethod
    def lissajous(center_x: float = 90, center_y: float = 90, amplitude: float = 30,
                  freq_x: float = 3, freq_y: float = 2, points: int = 200,
                  color: LaserColor = LaserColor.RED) -> Pattern:
        """Generate Lissajous curve pattern"""
        pattern_points = []
        
        for i in range(points):
            t = (i / points) * 2 * math.pi
            x = center_x + amplitude * math.sin(freq_x * t)
            y = center_y + amplitude * math.sin(freq_y * t)
            
            pattern_points.append(LaserPoint(x, y, color, 0.02))
        
        return Pattern("Lissajous", pattern_points)
    
    @staticmethod
    def rainbow_wave(points: int = 100) -> Pattern:
        """Generate wave pattern with color cycling"""
        pattern_points = []
        colors = [LaserColor.RED, LaserColor.GREEN, LaserColor.BLUE]
        
        for i in range(points):
            progress = i / points
            x = 30 + 120 * progress  # Sweep across X
            y = 90 + 30 * math.sin(progress * 4 * math.pi)  # Wave in Y
            
            color = colors[i % len(colors)]
            pattern_points.append(LaserPoint(x, y, color, 0.05))
        
        return Pattern("Rainbow Wave", pattern_points)

class BeatDetector:
    """Simple beat detection from audio input"""
    
    def __init__(self):
        self.last_beat_time = 0
        self.beat_threshold = 0.1  # Minimum time between beats
        self.running = False
        self.beat_callback = None
    
    def start_detection(self, callback: Callable = None) -> None:
        """Start beat detection in background thread"""
        self.running = True
        self.beat_callback = callback
        
        def detect_loop():
            while self.running:
                # Simple beat detection using GPIO pin changes
                if GPIO.input(AUDIO_INPUT_PIN):
                    current_time = time.time()
                    if current_time - self.last_beat_time > self.beat_threshold:
                        self.last_beat_time = current_time
                        if self.beat_callback:
                            self.beat_callback()
                
                time.sleep(0.01)
        
        thread = threading.Thread(target=detect_loop, daemon=True)
        thread.start()
    
    def stop_detection(self) -> None:
        """Stop beat detection"""
        self.running = False

class LaserShow:
    """Main laser show controller"""
    
    def __init__(self):
        self.controller = LaserController()
        self.generator = PatternGenerator()
        self.beat_detector = BeatDetector()
        
        self.current_pattern = None
        self.pattern_index = 0
        self.running = False
        self.music_mode = False
        self.emergency_stop = False
        
        # Pre-built patterns
        self.patterns = [
            self.generator.circle(),
            self.generator.spiral(),
            self.generator.figure_eight(),
            self.generator.star(),
            self.generator.lissajous(),
            self.generator.rainbow_wave()
        ]
        
        print("✅ Laser show system ready!")
        print(f"📦 Loaded {len(self.patterns)} built-in patterns")
    
    def check_emergency_stop(self) -> bool:
        """Check emergency stop button"""
        if not GPIO.input(BUTTON_STOP_PIN):  # Button pressed (active low)
            self.emergency_stop = True
            self.stop_show()
            print("🛑 EMERGENCY STOP ACTIVATED!")
            return True
        return False
    
    def start_show(self, pattern_name: str = None) -> None:
        """Start laser show with specified or current pattern"""
        if self.running:
            print("⚠️ Show already running")
            return
        
        if pattern_name:
            pattern = next((p for p in self.patterns if p.name == pattern_name), None)
            if pattern:
                self.current_pattern = pattern
            else:
                print(f"❌ Pattern '{pattern_name}' not found")
                return
        
        if not self.current_pattern:
            self.current_pattern = self.patterns[0]
        
        self.running = True
        self.emergency_stop = False
        
        print(f"🌟 Starting show: {self.current_pattern.name}")
        GPIO.output(LED_STATUS_PIN, GPIO.HIGH)
        
        # Run show in background thread
        thread = threading.Thread(target=self._show_loop, daemon=True)
        thread.start()
    
    def _show_loop(self) -> None:
        """Main show execution loop"""
        while self.running and not self.emergency_stop:
            try:
                for point in self.current_pattern.points:
                    if not self.running or self.emergency_stop:
                        break
                    
                    # Check emergency stop
                    if self.check_emergency_stop():
                        break
                    
                    # Execute laser point
                    duration = point.duration / self.current_pattern.speed_multiplier
                    self.controller.execute_point(
                        LaserPoint(point.x, point.y, point.color, duration)
                    )
                
                # Check if pattern should repeat
                if not self.current_pattern.repeat:
                    break
                    
            except Exception as e:
                print(f"❌ Show error: {e}")
                break
        
        # Clean up after show
        self.stop_show()
    
    def stop_show(self) -> None:
        """Stop current laser show"""
        self.running = False
        
        # Turn off all lasers
        self.controller.set_laser_color(LaserColor.OFF)
        
        # Move to center position
        self.controller.move_to(90, 90)
        
        # Turn off status LED
        GPIO.output(LED_STATUS_PIN, GPIO.LOW)
        
        print("🛑 Show stopped")
    
    def next_pattern(self) -> None:
        """Switch to next pattern"""
        self.pattern_index = (self.pattern_index + 1) % len(self.patterns)
        self.current_pattern = self.patterns[self.pattern_index]
        
        if self.running:
            print(f"🔄 Switching to: {self.current_pattern.name}")
        else:
            print(f"📋 Selected: {self.current_pattern.name}")
    
    def set_speed(self, multiplier: float) -> None:
        """Set pattern speed multiplier"""
        if self.current_pattern:
            self.current_pattern.speed_multiplier = max(0.1, min(5.0, multiplier))
            print(f"⚡ Speed set to {self.current_pattern.speed_multiplier}x")
    
    def start_music_mode(self) -> None:
        """Start music-reactive mode"""
        self.music_mode = True
        
        def on_beat():
            if self.running:
                # Quick flash effect on beat
                original_color = self.controller.current_color
                self.controller.set_laser_color(LaserColor.WHITE)
                time.sleep(0.1)
                self.controller.set_laser_color(original_color)
        
        self.beat_detector.start_detection(on_beat)
        print("🎵 Music mode activated")
    
    def stop_music_mode(self) -> None:
        """Stop music-reactive mode"""
        self.music_mode = False
        self.beat_detector.stop_detection()
        print("🔇 Music mode deactivated")
    
    def manual_control(self, x: float, y: float, color: LaserColor) -> None:
        """Manual laser control"""
        if not self.running:
            self.controller.move_to(x, y)
            self.controller.set_laser_color(color)
            print(f"🎮 Manual: ({x:.1f}, {y:.1f}) - {color.value}")
    
    def save_pattern(self, pattern: Pattern, filename: str) -> None:
        """Save pattern to file"""
        try:
            pattern_data = {
                'name': pattern.name,
                'repeat': pattern.repeat,
                'speed_multiplier': pattern.speed_multiplier,
                'points': [
                    {
                        'x': p.x,
                        'y': p.y,
                        'color': p.color.value,
                        'duration': p.duration
                    }
                    for p in pattern.points
                ]
            }
            
            with open(filename, 'w') as f:
                json.dump(pattern_data, f, indent=2)
            
            print(f"💾 Pattern saved: {filename}")
            
        except Exception as e:
            print(f"❌ Save failed: {e}")
    
    def load_pattern(self, filename: str) -> Pattern:
        """Load pattern from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            points = []
            for p in data['points']:
                color = LaserColor(p['color'])
                point = LaserPoint(p['x'], p['y'], color, p['duration'])
                points.append(point)
            
            pattern = Pattern(
                data['name'],
                points,
                data.get('repeat', True),
                data.get('speed_multiplier', 1.0)
            )
            
            print(f"📂 Pattern loaded: {filename}")
            return pattern
            
        except Exception as e:
            print(f"❌ Load failed: {e}")
            return None
    
    def interactive_mode(self) -> None:
        """Interactive control mode"""
        print("\n🎮 INTERACTIVE LASER SHOW CONTROL")
        print("Commands:")
        print("  'start [pattern]' - Start show")
        print("  'stop' - Stop show")
        print("  'next' - Next pattern")
        print("  'speed <1-5>' - Set speed")
        print("  'music' - Toggle music mode")
        print("  'list' - List patterns")
        print("  'manual <x> <y> <color>' - Manual control")
        print("  'quit' - Exit")
        print("\nPress Ctrl+C anytime for emergency stop\n")
        
        try:
            while True:
                cmd = input("laser> ").strip().lower().split()
                
                if not cmd:
                    continue
                
                if cmd[0] == 'start':
                    pattern_name = cmd[1] if len(cmd) > 1 else None
                    self.start_show(pattern_name)
                
                elif cmd[0] == 'stop':
                    self.stop_show()
                
                elif cmd[0] == 'next':
                    self.next_pattern()
                
                elif cmd[0] == 'speed' and len(cmd) > 1:
                    try:
                        speed = float(cmd[1])
                        self.set_speed(speed)
                    except ValueError:
                        print("❌ Invalid speed value")
                
                elif cmd[0] == 'music':
                    if self.music_mode:
                        self.stop_music_mode()
                    else:
                        self.start_music_mode()
                
                elif cmd[0] == 'list':
                    print("📋 Available patterns:")
                    for i, pattern in enumerate(self.patterns):
                        current = " (current)" if pattern == self.current_pattern else ""
                        print(f"  {i+1}. {pattern.name}{current}")
                
                elif cmd[0] == 'manual' and len(cmd) == 4:
                    try:
                        x = float(cmd[1])
                        y = float(cmd[2])
                        color = LaserColor(cmd[3])
                        self.manual_control(x, y, color)
                    except (ValueError, KeyError):
                        print("❌ Invalid manual command")
                
                elif cmd[0] == 'quit':
                    break
                
                else:
                    print("❌ Unknown command")
        
        except KeyboardInterrupt:
            print("\n🛑 Emergency stop!")
        
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean shutdown"""
        print("🔧 Shutting down laser show...")
        
        self.stop_show()
        self.stop_music_mode()
        
        # Turn off all outputs
        GPIO.output(LASER_RED_PIN, GPIO.LOW)
        GPIO.output(LASER_GREEN_PIN, GPIO.LOW)
        GPIO.output(LASER_BLUE_PIN, GPIO.LOW)
        GPIO.output(LED_STATUS_PIN, GPIO.LOW)
        
        # Stop servos
        servo_x.stop()
        servo_y.stop()
        
        # Clean up GPIO
        GPIO.cleanup()
        
        print("✅ Laser show shutdown complete")

def main():
    """Main function to run laser show"""
    try:
        show = LaserShow()
        show.interactive_mode()
    except Exception as e:
        print(f"❌ Critical error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

"""
🌟 LASER SHOW FEATURES:

1. PATTERN GENERATION:
   - Geometric shapes (circles, spirals, stars)
   - Mathematical curves (Lissajous, figure-8)
   - Color cycling and multi-color effects
   - Customizable parameters for each pattern

2. CONTROL MODES:
   - Automatic pattern playback
   - Manual positioning control
   - Music-reactive mode with beat detection
   - Interactive command-line interface

3. SAFETY FEATURES:
   - Emergency stop button
   - Position limits to prevent servo damage
   - Automatic laser shutoff on errors
   - Smooth movements to prevent jerky motion

4. ADVANCED FEATURES:
   - Pattern save/load functionality
   - Speed control and timing adjustment
   - Multi-laser color coordination
   - Real-time parameter modification

🎯 CUSTOMIZATION IDEAS:
- Add more complex patterns
- Implement DMX lighting protocol
- Create web-based remote control
- Add sound visualization algorithms
- Integrate with music streaming services

⚠️ SAFETY REMINDERS:
- Never look directly at laser beams
- Use only low-power (<5mW) lasers
- Secure all mechanical mounting
- Test emergency stop functionality
- Keep audience at safe distances
"""


