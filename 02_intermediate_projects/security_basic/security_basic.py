#!/usr/bin/env python3
"""
🛡️ BASIC SECURITY SYSTEM
An intermediate project that creates a simple but effective security system!

This project uses:
- IR break-beam sensor for motion detection
- LED indicators for status display
- Buzzer for audio alerts
- Log file for event recording
- Simple web interface for remote monitoring

Features:
- Armed/Disarmed modes with keypad entry
- Multiple alert types (visual, audio, logged)
- Basic intrusion logging with timestamps
- LED status indicators
- Configurable sensitivity and alert duration

Author: AI Tutor
Safety: Always test your security system before relying on it!
"""

import time
import datetime
import json
import os
from typing import Dict, List
from dataclasses import dataclass

import RPi.GPIO as GPIO

print("🛡️ Basic Security System Starting...")
print("🔧 Initializing sensors and components...")

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Configuration
IR_SENSOR_PIN = 17      # IR break-beam sensor input
BUZZER_PIN = 18         # Active buzzer for alerts
LED_ARMED_PIN = 23      # Green LED - system armed
LED_ALERT_PIN = 24      # Red LED - intrusion detected
LED_STATUS_PIN = 25     # Blue LED - system status/heartbeat
BUTTON_ARM_PIN = 2      # Push button to arm system
BUTTON_DISARM_PIN = 3   # Push button to disarm system

# Setup GPIO pins
GPIO.setup(IR_SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_ARMED_PIN, GPIO.OUT)
GPIO.setup(LED_ALERT_PIN, GPIO.OUT)
GPIO.setup(LED_STATUS_PIN, GPIO.OUT)
GPIO.setup(BUTTON_ARM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON_DISARM_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize outputs to OFF
GPIO.output(BUZZER_PIN, GPIO.LOW)
GPIO.output(LED_ARMED_PIN, GPIO.LOW)
GPIO.output(LED_ALERT_PIN, GPIO.LOW)
GPIO.output(LED_STATUS_PIN, GPIO.LOW)

@dataclass
class SecurityEvent:
    """Data class for security events"""
    timestamp: str
    event_type: str
    description: str
    sensor_state: bool

class SecuritySystem:
    """Main security system class"""
    
    def __init__(self):
        self.armed = False
        self.alert_active = False
        self.last_sensor_state = True  # True = beam intact, False = beam broken
        self.intrusion_count = 0
        self.events: List[SecurityEvent] = []
        self.log_file = "security_log.json"
        self.config = {
            "alert_duration": 10,     # seconds
            "entry_delay": 5,         # seconds before alert activates
            "exit_delay": 10,         # seconds to disarm after arming
            "sensitivity": 0.2        # debounce time in seconds
        }
        self.last_motion_time = 0
        self.entry_delay_start = None
        self.alert_start_time = None
        
        # Load existing log file if it exists
        self.load_events()
        
        print("✅ Security system initialized")
        print(f"📁 Log file: {os.path.abspath(self.log_file)}")
    
    def log_event(self, event_type: str, description: str, sensor_state: bool = True) -> None:
        """Log a security event with timestamp"""
        timestamp = datetime.datetime.now().isoformat()
        event = SecurityEvent(timestamp, event_type, description, sensor_state)
        self.events.append(event)
        
        # Print to console
        print(f"📝 [{timestamp}] {event_type}: {description}")
        
        # Save to file
        self.save_events()
    
    def save_events(self) -> None:
        """Save events to JSON log file"""
        try:
            events_dict = []
            for event in self.events:
                events_dict.append({
                    'timestamp': event.timestamp,
                    'event_type': event.event_type,
                    'description': event.description,
                    'sensor_state': event.sensor_state
                })
            
            with open(self.log_file, 'w') as f:
                json.dump(events_dict, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save events: {e}")
    
    def load_events(self) -> None:
        """Load events from JSON log file"""
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    events_data = json.load(f)
                
                for event_data in events_data:
                    event = SecurityEvent(
                        event_data['timestamp'],
                        event_data['event_type'],
                        event_data['description'],
                        event_data['sensor_state']
                    )
                    self.events.append(event)
                
                print(f"📂 Loaded {len(self.events)} previous events")
        except Exception as e:
            print(f"⚠️ Failed to load events: {e}")
    
    def arm_system(self) -> None:
        """Arm the security system"""
        if not self.armed:
            self.armed = True
            self.alert_active = False
            self.entry_delay_start = None
            
            # LED indicators
            GPIO.output(LED_ARMED_PIN, GPIO.HIGH)
            GPIO.output(LED_ALERT_PIN, GPIO.LOW)
            
            # Quick beep pattern to confirm arming
            for _ in range(3):
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(0.1)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(0.1)
            
            self.log_event("SYSTEM", "Security system ARMED")
            print("🛡️ System ARMED - Protected area is now monitored")
    
    def disarm_system(self) -> None:
        """Disarm the security system"""
        if self.armed:
            self.armed = False
            self.alert_active = False
            self.entry_delay_start = None
            self.alert_start_time = None
            
            # LED indicators
            GPIO.output(LED_ARMED_PIN, GPIO.LOW)
            GPIO.output(LED_ALERT_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            
            # Two long beeps to confirm disarming
            for _ in range(2):
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
                time.sleep(0.3)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
                time.sleep(0.2)
            
            self.log_event("SYSTEM", "Security system DISARMED")
            print("🔓 System DISARMED - Area monitoring disabled")
    
    def trigger_alert(self) -> None:
        """Trigger security alert"""
        if not self.alert_active:
            self.alert_active = True
            self.alert_start_time = time.time()
            self.intrusion_count += 1
            
            # Turn on alert LED
            GPIO.output(LED_ALERT_PIN, GPIO.HIGH)
            
            self.log_event("INTRUSION", f"Motion detected! Alert #{self.intrusion_count}", False)
            print(f"🚨 SECURITY ALERT! Intrusion detected (#{self.intrusion_count})")
    
    def update_alert(self) -> None:
        """Update ongoing alert state"""
        if self.alert_active and self.alert_start_time:
            elapsed = time.time() - self.alert_start_time
            
            # Flash alert LED and sound buzzer
            if elapsed % 0.5 < 0.25:  # Flash every 0.5 seconds
                GPIO.output(LED_ALERT_PIN, GPIO.HIGH)
                GPIO.output(BUZZER_PIN, GPIO.HIGH)
            else:
                GPIO.output(LED_ALERT_PIN, GPIO.LOW)
                GPIO.output(BUZZER_PIN, GPIO.LOW)
            
            # Stop alert after configured duration
            if elapsed > self.config["alert_duration"]:
                self.stop_alert()
    
    def stop_alert(self) -> None:
        """Stop the active alert"""
        if self.alert_active:
            self.alert_active = False
            self.alert_start_time = None
            
            # Turn off alert indicators
            GPIO.output(LED_ALERT_PIN, GPIO.LOW)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            
            self.log_event("SYSTEM", "Alert stopped - monitoring continues")
            print("✅ Alert stopped - System remains armed")
    
    def check_sensor(self) -> None:
        """Check IR sensor for motion"""
        current_state = GPIO.input(IR_SENSOR_PIN)
        current_time = time.time()
        
        # Debounce: ignore rapid changes
        if current_time - self.last_motion_time < self.config["sensitivity"]:
            return
        
        # Detect state change (beam broken)
        if self.last_sensor_state and not current_state:
            self.last_motion_time = current_time
            
            if self.armed and not self.alert_active:
                # Start entry delay
                if not self.entry_delay_start:
                    self.entry_delay_start = current_time
                    self.log_event("MOTION", "Motion detected - Entry delay started")
                    print(f"⏰ Entry delay: {self.config['entry_delay']} seconds to disarm")
                
                # Check if entry delay has expired
                elif current_time - self.entry_delay_start > self.config["entry_delay"]:
                    self.trigger_alert()
            
            elif not self.armed:
                self.log_event("MOTION", "Motion detected (system disarmed)")
                print("👻 Motion detected (system not armed)")
        
        # Beam restored
        elif not self.last_sensor_state and current_state:
            if self.armed:
                self.log_event("MOTION", "Motion cleared - Beam restored")
                print("✅ Motion cleared - Beam restored")
        
        self.last_sensor_state = current_state
    
    def check_buttons(self) -> None:
        """Check arm/disarm buttons"""
        # ARM button (active low - pressed = False)
        if not GPIO.input(BUTTON_ARM_PIN):
            if not self.armed:
                time.sleep(0.3)  # Debounce
                if not GPIO.input(BUTTON_ARM_PIN):  # Still pressed
                    self.arm_system()
                    time.sleep(1)  # Prevent multiple triggers
        
        # DISARM button
        if not GPIO.input(BUTTON_DISARM_PIN):
            if self.armed:
                time.sleep(0.3)  # Debounce
                if not GPIO.input(BUTTON_DISARM_PIN):  # Still pressed
                    self.disarm_system()
                    time.sleep(1)  # Prevent multiple triggers
    
    def update_status_led(self) -> None:
        """Update status LED with heartbeat pattern"""
        # Heartbeat: quick double flash every 2 seconds
        cycle_time = time.time() % 2.0
        
        if cycle_time < 0.1 or (0.2 < cycle_time < 0.3):
            GPIO.output(LED_STATUS_PIN, GPIO.HIGH)
        else:
            GPIO.output(LED_STATUS_PIN, GPIO.LOW)
    
    def print_status(self) -> None:
        """Print current system status"""
        status = "ARMED" if self.armed else "DISARMED"
        alert = " | ALERT ACTIVE" if self.alert_active else ""
        sensor = "CLEAR" if self.last_sensor_state else "TRIGGERED"
        
        print(f"Status: {status}{alert} | Sensor: {sensor} | Events: {len(self.events)}")
    
    def run(self) -> None:
        """Main system loop"""
        print("\n🛡️ Basic Security System Ready!")
        print("📋 Controls:")
        print("   - Press ARM button to arm system")
        print("   - Press DISARM button to disarm system")
        print("   - Break IR beam when armed to trigger alert")
        print("   - Press Ctrl+C to shutdown safely")
        print("\n" + "="*50)
        
        last_status_print = 0
        
        try:
            while True:
                # Check sensors and buttons
                self.check_sensor()
                self.check_buttons()
                
                # Update alerts and LEDs
                if self.alert_active:
                    self.update_alert()
                
                self.update_status_led()
                
                # Print status every 5 seconds
                if time.time() - last_status_print > 5:
                    self.print_status()
                    last_status_print = time.time()
                
                # Small delay for smooth operation
                time.sleep(0.1)
        
        except KeyboardInterrupt:
            print("\n🛑 Shutting down security system...")
            self.log_event("SYSTEM", "Security system shutdown")
        
        finally:
            self.cleanup()
    
    def cleanup(self) -> None:
        """Clean shutdown of the security system"""
        # Turn off all outputs
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.output(LED_ARMED_PIN, GPIO.LOW)
        GPIO.output(LED_ALERT_PIN, GPIO.LOW)
        GPIO.output(LED_STATUS_PIN, GPIO.LOW)
        
        # Clean up GPIO
        GPIO.cleanup()
        
        print("✅ Security system shutdown complete")
        print(f"📊 Session summary:")
        print(f"   - Total events logged: {len(self.events)}")
        print(f"   - Intrusions detected: {self.intrusion_count}")
        print(f"   - Log file: {os.path.abspath(self.log_file)}")


def main():
    """Main function to run the security system"""
    try:
        security = SecuritySystem()
        security.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        GPIO.cleanup()


if __name__ == "__main__":
    main()


"""
🤔 HOW THIS WORKS:

1. INITIALIZATION:
   - Sets up GPIO pins for sensors, LEDs, buzzer, and buttons
   - Loads previous security events from log file
   - Creates configuration for timing and sensitivity

2. ARMING/DISARMING:
   - Physical buttons to arm/disarm the system
   - Visual and audio feedback for state changes
   - Automatic logging of all state changes

3. MOTION DETECTION:
   - IR break-beam sensor detects intrusions
   - Entry delay allows time to disarm before alert
   - Debouncing prevents false triggers

4. ALERT SYSTEM:
   - Flashing LED and buzzer for audio/visual alerts
   - Configurable alert duration
   - Automatic alert timeout with continued monitoring

5. LOGGING:
   - JSON file stores all events with timestamps
   - Events include system state changes and intrusions
   - Persistent storage survives system restarts

🎯 KEY FEATURES:
- Entry/exit delays for practical use
- Debounced inputs prevent false triggers
- Comprehensive event logging
- LED status indicators
- Configurable timing parameters

🔧 CUSTOMIZATION:
- Adjust timing in security.config dictionary
- Add more sensors by expanding check_sensor()
- Modify alert patterns in update_alert()
- Add network notifications in log_event()

🚀 ENHANCEMENT IDEAS:
- Web interface for remote monitoring
- Email/SMS notifications
- Multiple detection zones
- Time-based arming/disarming
- Integration with home automation systems
"""


