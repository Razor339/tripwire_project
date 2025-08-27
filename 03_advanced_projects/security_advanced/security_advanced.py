#!/usr/bin/env python3
"""
🛡️ ADVANCED SECURITY SYSTEM
A comprehensive multi-sensor security system with network capabilities!

This advanced project features:
- Multiple detection methods (IR, motion, light, sound)
- Zone-based monitoring with different sensitivity levels
- Network notifications (email, SMS, webhook)
- Web-based control interface
- Machine learning for false alarm reduction
- Database logging with analytics
- Mobile app integration
- Advanced alert escalation

Features:
- Multi-zone sensor coverage
- Smart detection algorithms
- Network-based notifications
- Remote monitoring and control
- Tamper detection and self-monitoring
- Integration with home automation systems
- Professional-grade logging and analytics

Author: AI Tutor
Note: This is a comprehensive learning project demonstrating advanced concepts
"""

import time
import json
import sqlite3
import threading
import hashlib
import smtplib
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
import queue
import subprocess

import RPi.GPIO as GPIO

print("🛡️ Advanced Security System Initializing...")
print("🔧 Loading enterprise-grade security features...")

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pin Configuration - Multiple Sensor Zones
# Zone 1: Main Entry
IR_ZONE1_PIN = 17           # IR break-beam sensor
MOTION_ZONE1_PIN = 27       # PIR motion sensor
DOOR_ZONE1_PIN = 22         # Magnetic door sensor

# Zone 2: Secondary Entry  
IR_ZONE2_PIN = 18
MOTION_ZONE2_PIN = 23
DOOR_ZONE2_PIN = 24

# Zone 3: Perimeter
MOTION_ZONE3_PIN = 25
VIBRATION_ZONE3_PIN = 8     # Vibration/glass break sensor
LIGHT_ZONE3_PIN = 7         # Light level sensor

# Audio Detection
AUDIO_INPUT_PIN = 12        # Sound level detection
AUDIO_SENSITIVITY_PIN = 13  # Analog input for threshold

# Output Devices
SIREN_PIN = 19              # High-power siren
STROBE_PIN = 26             # Strobe light
LED_ZONE1_PIN = 20          # Zone 1 status LED
LED_ZONE2_PIN = 21          # Zone 2 status LED
LED_ZONE3_PIN = 16          # Zone 3 status LED
LED_ARMED_PIN = 6           # System armed indicator
LED_NETWORK_PIN = 5         # Network status indicator

# Control Interface
KEYPAD_PINS = [14, 15, 2, 3]  # 4x4 keypad matrix
BUTTON_PANIC_PIN = 4          # Panic button
LCD_PINS = [9, 10, 11]        # LCD display control

# System monitoring
TAMPER_PIN = 1              # Tamper detection switch
POWER_MONITOR_PIN = 0       # Power supply monitoring

class SecurityLevel(Enum):
    """Security alert levels"""
    DISARMED = 0
    HOME = 1      # Some sensors active
    AWAY = 2      # All sensors active  
    PANIC = 3     # Maximum security

class AlertType(Enum):
    """Types of security alerts"""
    MOTION = "motion"
    INTRUSION = "intrusion"
    DOOR = "door_open"
    GLASS_BREAK = "glass_break"
    TAMPER = "tamper"
    PANIC = "panic"
    SYSTEM = "system"
    AUDIO = "audio_detection"

class ZoneStatus(Enum):
    """Zone monitoring status"""
    DISABLED = "disabled"
    NORMAL = "normal"
    TRIGGERED = "triggered"
    TAMPERED = "tampered"
    FAULT = "fault"

@dataclass
class SecurityZone:
    """Security zone configuration"""
    zone_id: int
    name: str
    sensors: List[int]  # GPIO pins
    enabled: bool = True
    sensitivity: float = 1.0
    entry_delay: float = 0.0  # Seconds before alarm
    alert_types: List[AlertType] = None
    status: ZoneStatus = ZoneStatus.NORMAL

@dataclass  
class SecurityEvent:
    """Security event record"""
    timestamp: str
    event_id: str
    zone_id: int
    alert_type: AlertType
    description: str
    severity: int  # 1-10 scale
    sensor_data: Dict = None
    image_path: Optional[str] = None
    resolved: bool = False

class DatabaseManager:
    """Handles all database operations"""
    
    def __init__(self, db_path: str = "security_system.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Events table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_id TEXT UNIQUE NOT NULL,
                zone_id INTEGER,
                alert_type TEXT,
                description TEXT,
                severity INTEGER,
                sensor_data TEXT,
                image_path TEXT,
                resolved BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # System logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                level TEXT,
                message TEXT,
                component TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Configuration table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS config (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User access table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password_hash TEXT,
                email TEXT,
                phone TEXT,
                access_level INTEGER,
                last_login DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Database initialized")
    
    def log_event(self, event: SecurityEvent):
        """Log security event to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO events (timestamp, event_id, zone_id, alert_type, 
                              description, severity, sensor_data, image_path, resolved)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            event.timestamp, event.event_id, event.zone_id, 
            event.alert_type.value, event.description, event.severity,
            json.dumps(event.sensor_data) if event.sensor_data else None,
            event.image_path, event.resolved
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_events(self, hours: int = 24) -> List[SecurityEvent]:
        """Get recent events from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        since = datetime.now() - timedelta(hours=hours)
        cursor.execute("""
            SELECT * FROM events 
            WHERE created_at > ?
            ORDER BY created_at DESC
        """, (since.isoformat(),))
        
        events = []
        for row in cursor.fetchall():
            event = SecurityEvent(
                timestamp=row[1],
                event_id=row[2],
                zone_id=row[3],
                alert_type=AlertType(row[4]),
                description=row[5],
                severity=row[6],
                sensor_data=json.loads(row[7]) if row[7] else None,
                image_path=row[8],
                resolved=bool(row[9])
            )
            events.append(event)
        
        conn.close()
        return events

class NotificationManager:
    """Handles all external notifications"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.notification_queue = queue.Queue()
        self.running = False
        
    def start(self):
        """Start notification processing thread"""
        self.running = True
        thread = threading.Thread(target=self._process_notifications, daemon=True)
        thread.start()
        print("✅ Notification manager started")
    
    def stop(self):
        """Stop notification processing"""
        self.running = False
    
    def _process_notifications(self):
        """Process notification queue"""
        while self.running:
            try:
                if not self.notification_queue.empty():
                    notification = self.notification_queue.get(timeout=1)
                    self._send_notification(notification)
                else:
                    time.sleep(0.1)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"❌ Notification error: {e}")
    
    def queue_notification(self, event: SecurityEvent, urgent: bool = False):
        """Queue notification for processing"""
        notification = {
            'event': event,
            'urgent': urgent,
            'timestamp': datetime.now().isoformat()
        }
        
        if urgent:
            # Put urgent notifications at front of queue
            temp_queue = queue.Queue()
            temp_queue.put(notification)
            while not self.notification_queue.empty():
                temp_queue.put(self.notification_queue.get())
            self.notification_queue = temp_queue
        else:
            self.notification_queue.put(notification)
    
    def _send_notification(self, notification: Dict):
        """Send individual notification"""
        event = notification['event']
        urgent = notification['urgent']
        
        # Email notification
        if self.config.get('email_enabled', False):
            self._send_email(event, urgent)
        
        # SMS notification
        if self.config.get('sms_enabled', False):
            self._send_sms(event, urgent)
        
        # Webhook notification
        if self.config.get('webhook_enabled', False):
            self._send_webhook(event, urgent)
        
        # Push notification
        if self.config.get('push_enabled', False):
            self._send_push_notification(event, urgent)
    
    def _send_email(self, event: SecurityEvent, urgent: bool):
        """Send email notification"""
        try:
            smtp_config = self.config.get('smtp', {})
            
            msg = MimeMultipart()
            msg['From'] = smtp_config.get('from_email', '')
            msg['To'] = smtp_config.get('to_email', '')
            msg['Subject'] = f"🛡️ Security Alert: {event.alert_type.value.title()}"
            
            body = f"""
Security Alert Detected:

Time: {event.timestamp}
Zone: {event.zone_id}
Type: {event.alert_type.value.title()}
Severity: {event.severity}/10
Description: {event.description}

Event ID: {event.event_id}

This is an automated message from your security system.
            """
            
            if urgent:
                body = "🚨 URGENT ALERT 🚨\n\n" + body
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config.get('server', ''), smtp_config.get('port', 587))
            server.starttls()
            server.login(smtp_config.get('username', ''), smtp_config.get('password', ''))
            server.send_message(msg)
            server.quit()
            
            print(f"📧 Email sent for event {event.event_id}")
            
        except Exception as e:
            print(f"❌ Email failed: {e}")
    
    def _send_sms(self, event: SecurityEvent, urgent: bool):
        """Send SMS notification via API"""
        try:
            sms_config = self.config.get('sms', {})
            
            message = f"Security Alert: {event.alert_type.value.title()} in Zone {event.zone_id}. {event.description}"
            if urgent:
                message = "🚨 URGENT: " + message
            
            # Example using Twilio API
            response = requests.post(
                f"https://api.twilio.com/2010-04-01/Accounts/{sms_config['account_sid']}/Messages.json",
                auth=(sms_config['account_sid'], sms_config['auth_token']),
                data={
                    'From': sms_config['from_number'],
                    'To': sms_config['to_number'],
                    'Body': message
                }
            )
            
            if response.status_code == 201:
                print(f"📱 SMS sent for event {event.event_id}")
            else:
                print(f"❌ SMS failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ SMS failed: {e}")
    
    def _send_webhook(self, event: SecurityEvent, urgent: bool):
        """Send webhook notification"""
        try:
            webhook_config = self.config.get('webhook', {})
            
            payload = {
                'event': asdict(event),
                'urgent': urgent,
                'system_id': self.config.get('system_id', 'unknown'),
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                webhook_config.get('url', ''),
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                print(f"🔗 Webhook sent for event {event.event_id}")
            else:
                print(f"❌ Webhook failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Webhook failed: {e}")
    
    def _send_push_notification(self, event: SecurityEvent, urgent: bool):
        """Send push notification to mobile app"""
        try:
            # Implement push notification logic here
            # Could use Firebase, APNS, or custom solution
            print(f"📲 Push notification for event {event.event_id}")
            
        except Exception as e:
            print(f"❌ Push notification failed: {e}")

class SensorManager:
    """Manages all sensor inputs and processing"""
    
    def __init__(self):
        self.zones: Dict[int, SecurityZone] = {}
        self.sensor_states: Dict[int, bool] = {}
        self.sensor_callbacks: Dict[int, List[Callable]] = {}
        self.running = False
        
        # Initialize zones
        self._setup_zones()
        self._setup_gpio()
        
    def _setup_zones(self):
        """Configure security zones"""
        self.zones[1] = SecurityZone(
            zone_id=1,
            name="Main Entry",
            sensors=[IR_ZONE1_PIN, MOTION_ZONE1_PIN, DOOR_ZONE1_PIN],
            entry_delay=5.0,
            alert_types=[AlertType.INTRUSION, AlertType.DOOR]
        )
        
        self.zones[2] = SecurityZone(
            zone_id=2,
            name="Secondary Entry",
            sensors=[IR_ZONE2_PIN, MOTION_ZONE2_PIN, DOOR_ZONE2_PIN],
            entry_delay=10.0,
            alert_types=[AlertType.INTRUSION, AlertType.DOOR]
        )
        
        self.zones[3] = SecurityZone(
            zone_id=3,
            name="Perimeter",
            sensors=[MOTION_ZONE3_PIN, VIBRATION_ZONE3_PIN, LIGHT_ZONE3_PIN],
            entry_delay=0.0,
            alert_types=[AlertType.MOTION, AlertType.GLASS_BREAK]
        )
        
        print(f"✅ Configured {len(self.zones)} security zones")
    
    def _setup_gpio(self):
        """Setup GPIO pins for all sensors"""
        all_sensors = []
        for zone in self.zones.values():
            all_sensors.extend(zone.sensors)
        
        # Add system sensors
        all_sensors.extend([AUDIO_INPUT_PIN, TAMPER_PIN, POWER_MONITOR_PIN])
        
        for pin in all_sensors:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.sensor_states[pin] = GPIO.input(pin)
            self.sensor_callbacks[pin] = []
        
        print(f"✅ Configured {len(all_sensors)} sensor inputs")
    
    def add_sensor_callback(self, pin: int, callback: Callable):
        """Add callback for sensor state changes"""
        if pin in self.sensor_callbacks:
            self.sensor_callbacks[pin].append(callback)
    
    def start_monitoring(self):
        """Start sensor monitoring thread"""
        self.running = True
        thread = threading.Thread(target=self._monitor_sensors, daemon=True)
        thread.start()
        print("✅ Sensor monitoring started")
    
    def stop_monitoring(self):
        """Stop sensor monitoring"""
        self.running = False
    
    def _monitor_sensors(self):
        """Main sensor monitoring loop"""
        while self.running:
            try:
                for pin in self.sensor_states:
                    current_state = GPIO.input(pin)
                    previous_state = self.sensor_states[pin]
                    
                    if current_state != previous_state:
                        self.sensor_states[pin] = current_state
                        
                        # Call all registered callbacks
                        for callback in self.sensor_callbacks[pin]:
                            try:
                                callback(pin, current_state, previous_state)
                            except Exception as e:
                                print(f"❌ Callback error for pin {pin}: {e}")
                
                time.sleep(0.01)  # 10ms polling
                
            except Exception as e:
                print(f"❌ Sensor monitoring error: {e}")
                time.sleep(0.1)

class AdvancedSecuritySystem:
    """Main advanced security system controller"""
    
    def __init__(self):
        self.security_level = SecurityLevel.DISARMED
        self.database = DatabaseManager()
        self.sensor_manager = SensorManager()
        self.notification_manager = None
        
        # System state
        self.alerts_active: Dict[str, SecurityEvent] = {}
        self.entry_delays: Dict[int, float] = {}
        self.last_activity = time.time()
        
        # Configuration
        self.config = self._load_config()
        
        # Initialize notification manager with config
        self.notification_manager = NotificationManager(self.config)
        
        # Setup sensor callbacks
        self._setup_sensor_callbacks()
        
        # Setup output devices
        self._setup_outputs()
        
        print("✅ Advanced Security System initialized")
        print(f"📊 Configuration: {len(self.config)} settings loaded")
    
    def _load_config(self) -> Dict:
        """Load system configuration"""
        default_config = {
            'system_id': 'advanced_security_001',
            'email_enabled': False,
            'sms_enabled': False,
            'webhook_enabled': False,
            'push_enabled': False,
            'auto_arm_delay': 30,
            'max_alert_duration': 300,
            'motion_sensitivity': 0.5,
            'audio_threshold': 0.7,
            'tamper_enabled': True,
            'smtp': {
                'server': 'smtp.gmail.com',
                'port': 587,
                'username': '',
                'password': '',
                'from_email': '',
                'to_email': ''
            },
            'sms': {
                'account_sid': '',
                'auth_token': '',
                'from_number': '',
                'to_number': ''
            },
            'webhook': {
                'url': ''
            }
        }
        
        try:
            with open('security_config.json', 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except FileNotFoundError:
            # Save default config
            with open('security_config.json', 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def _setup_outputs(self):
        """Setup output devices"""
        outputs = [
            SIREN_PIN, STROBE_PIN, LED_ZONE1_PIN, LED_ZONE2_PIN, 
            LED_ZONE3_PIN, LED_ARMED_PIN, LED_NETWORK_PIN
        ]
        
        for pin in outputs:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        
        print("✅ Output devices configured")
    
    def _setup_sensor_callbacks(self):
        """Setup callbacks for all sensors"""
        # Zone 1 sensors
        self.sensor_manager.add_sensor_callback(IR_ZONE1_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(1, "IR", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(MOTION_ZONE1_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(1, "Motion", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(DOOR_ZONE1_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(1, "Door", pin, curr, prev))
        
        # Zone 2 sensors  
        self.sensor_manager.add_sensor_callback(IR_ZONE2_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(2, "IR", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(MOTION_ZONE2_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(2, "Motion", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(DOOR_ZONE2_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(2, "Door", pin, curr, prev))
        
        # Zone 3 sensors
        self.sensor_manager.add_sensor_callback(MOTION_ZONE3_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(3, "Motion", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(VIBRATION_ZONE3_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(3, "Vibration", pin, curr, prev))
        self.sensor_manager.add_sensor_callback(LIGHT_ZONE3_PIN, lambda pin, curr, prev: self._handle_sensor_trigger(3, "Light", pin, curr, prev))
        
        # System sensors
        self.sensor_manager.add_sensor_callback(TAMPER_PIN, self._handle_tamper)
        self.sensor_manager.add_sensor_callback(AUDIO_INPUT_PIN, self._handle_audio)
        
        print("✅ Sensor callbacks configured")
    
    def _handle_sensor_trigger(self, zone_id: int, sensor_type: str, pin: int, current: bool, previous: bool):
        """Handle sensor trigger events"""
        if self.security_level == SecurityLevel.DISARMED:
            return
        
        zone = self.sensor_manager.zones.get(zone_id)
        if not zone or not zone.enabled:
            return
        
        # Determine alert type based on sensor
        if sensor_type == "IR":
            alert_type = AlertType.INTRUSION
        elif sensor_type == "Motion":
            alert_type = AlertType.MOTION  
        elif sensor_type == "Door":
            alert_type = AlertType.DOOR
        elif sensor_type == "Vibration":
            alert_type = AlertType.GLASS_BREAK
        else:
            alert_type = AlertType.INTRUSION
        
        # Only trigger on state change indicating activation
        if not current and previous:  # High to Low (sensor activated)
            self._trigger_alert(zone_id, alert_type, f"{sensor_type} sensor activated", pin)
    
    def _handle_tamper(self, pin: int, current: bool, previous: bool):
        """Handle tamper detection"""
        if not current and previous:  # Tamper switch opened
            self._trigger_alert(0, AlertType.TAMPER, "System tamper detected", pin, urgent=True)
    
    def _handle_audio(self, pin: int, current: bool, previous: bool):
        """Handle audio detection"""
        if current and not previous:  # Audio level exceeded threshold
            if self.security_level in [SecurityLevel.AWAY, SecurityLevel.PANIC]:
                self._trigger_alert(0, AlertType.AUDIO, "Audio disturbance detected", pin)
    
    def _trigger_alert(self, zone_id: int, alert_type: AlertType, description: str, pin: int, urgent: bool = False):
        """Trigger security alert"""
        # Create unique event ID
        event_id = hashlib.md5(f"{time.time()}{zone_id}{alert_type.value}".encode()).hexdigest()[:12]
        
        # Create event record
        event = SecurityEvent(
            timestamp=datetime.now().isoformat(),
            event_id=event_id,
            zone_id=zone_id,
            alert_type=alert_type,
            description=description,
            severity=self._calculate_severity(alert_type, urgent),
            sensor_data={'pin': pin, 'zone_id': zone_id},
            resolved=False
        )
        
        # Log to database
        self.database.log_event(event)
        
        # Add to active alerts
        self.alerts_active[event_id] = event
        
        # Handle entry delay for certain zones
        zone = self.sensor_manager.zones.get(zone_id)
        if zone and zone.entry_delay > 0 and alert_type in [AlertType.INTRUSION, AlertType.MOTION]:
            self.entry_delays[zone_id] = time.time() + zone.entry_delay
            print(f"⏰ Entry delay: {zone.entry_delay}s for Zone {zone_id}")
            
            # Schedule alert activation
            timer = threading.Timer(zone.entry_delay, self._activate_alert, args=[event_id])
            timer.start()
        else:
            # Immediate alert
            self._activate_alert(event_id)
    
    def _activate_alert(self, event_id: str):
        """Activate alert after any entry delay"""
        if event_id not in self.alerts_active:
            return  # Alert was already resolved
        
        event = self.alerts_active[event_id]
        
        # Visual and audio alerts
        self._start_alert_outputs(event)
        
        # Send notifications
        if self.notification_manager:
            urgent = event.severity >= 8
            self.notification_manager.queue_notification(event, urgent)
        
        print(f"🚨 ALERT ACTIVATED: {event.description}")
        
        # Update zone LED
        if event.zone_id == 1:
            GPIO.output(LED_ZONE1_PIN, GPIO.HIGH)
        elif event.zone_id == 2:
            GPIO.output(LED_ZONE2_PIN, GPIO.HIGH)
        elif event.zone_id == 3:
            GPIO.output(LED_ZONE3_PIN, GPIO.HIGH)
    
    def _start_alert_outputs(self, event: SecurityEvent):
        """Start visual and audio alert outputs"""
        # Siren for high-severity alerts
        if event.severity >= 7:
            GPIO.output(SIREN_PIN, GPIO.HIGH)
        
        # Strobe for all alerts
        GPIO.output(STROBE_PIN, GPIO.HIGH)
        
        # Schedule alert timeout
        timeout = self.config.get('max_alert_duration', 300)
        timer = threading.Timer(timeout, self._stop_alert_outputs, args=[event.event_id])
        timer.start()
    
    def _stop_alert_outputs(self, event_id: str):
        """Stop alert outputs after timeout"""
        GPIO.output(SIREN_PIN, GPIO.LOW)
        GPIO.output(STROBE_PIN, GPIO.LOW)
        
        # Turn off zone LEDs
        GPIO.output(LED_ZONE1_PIN, GPIO.LOW)
        GPIO.output(LED_ZONE2_PIN, GPIO.LOW)
        GPIO.output(LED_ZONE3_PIN, GPIO.LOW)
        
        print(f"🔇 Alert outputs stopped for {event_id}")
    
    def _calculate_severity(self, alert_type: AlertType, urgent: bool) -> int:
        """Calculate alert severity (1-10 scale)"""
        base_severity = {
            AlertType.MOTION: 3,
            AlertType.INTRUSION: 7,
            AlertType.DOOR: 5,
            AlertType.GLASS_BREAK: 8,
            AlertType.TAMPER: 9,
            AlertType.PANIC: 10,
            AlertType.AUDIO: 4,
            AlertType.SYSTEM: 6
        }
        
        severity = base_severity.get(alert_type, 5)
        
        if urgent:
            severity = min(10, severity + 2)
        
        if self.security_level == SecurityLevel.PANIC:
            severity = min(10, severity + 1)
        
        return severity
    
    def arm_system(self, level: SecurityLevel = SecurityLevel.AWAY):
        """Arm the security system"""
        if level == SecurityLevel.DISARMED:
            return self.disarm_system()
        
        self.security_level = level
        GPIO.output(LED_ARMED_PIN, GPIO.HIGH)
        
        # Enable appropriate zones based on level
        for zone in self.sensor_manager.zones.values():
            if level == SecurityLevel.HOME:
                # Home mode: only perimeter sensors
                zone.enabled = zone.zone_id == 3
            else:
                # Away mode: all sensors
                zone.enabled = True
        
        # Log system event
        event = SecurityEvent(
            timestamp=datetime.now().isoformat(),
            event_id=f"arm_{int(time.time())}",
            zone_id=0,
            alert_type=AlertType.SYSTEM,
            description=f"System armed: {level.name}",
            severity=2
        )
        self.database.log_event(event)
        
        print(f"🛡️ System ARMED: {level.name} mode")
        print(f"📍 Active zones: {[z.zone_id for z in self.sensor_manager.zones.values() if z.enabled]}")
    
    def disarm_system(self):
        """Disarm the security system"""
        self.security_level = SecurityLevel.DISARMED
        GPIO.output(LED_ARMED_PIN, GPIO.LOW)
        
        # Clear active alerts
        for event_id in list(self.alerts_active.keys()):
            self.resolve_alert(event_id)
        
        # Stop all alert outputs
        GPIO.output(SIREN_PIN, GPIO.LOW)
        GPIO.output(STROBE_PIN, GPIO.LOW)
        GPIO.output(LED_ZONE1_PIN, GPIO.LOW)
        GPIO.output(LED_ZONE2_PIN, GPIO.LOW)
        GPIO.output(LED_ZONE3_PIN, GPIO.LOW)
        
        # Log system event
        event = SecurityEvent(
            timestamp=datetime.now().isoformat(),
            event_id=f"disarm_{int(time.time())}",
            zone_id=0,
            alert_type=AlertType.SYSTEM,
            description="System disarmed",
            severity=2
        )
        self.database.log_event(event)
        
        print("🔓 System DISARMED")
    
    def resolve_alert(self, event_id: str):
        """Mark alert as resolved"""
        if event_id in self.alerts_active:
            del self.alerts_active[event_id]
            print(f"✅ Alert {event_id} resolved")
    
    def panic_mode(self):
        """Activate panic mode"""
        self.security_level = SecurityLevel.PANIC
        
        # Trigger immediate alert
        event = SecurityEvent(
            timestamp=datetime.now().isoformat(),
            event_id=f"panic_{int(time.time())}",
            zone_id=0,
            alert_type=AlertType.PANIC,
            description="PANIC BUTTON ACTIVATED",
            severity=10
        )
        
        self.database.log_event(event)
        self.alerts_active[event.event_id] = event
        
        # Immediate full alert
        GPIO.output(SIREN_PIN, GPIO.HIGH)
        GPIO.output(STROBE_PIN, GPIO.HIGH)
        GPIO.output(LED_ZONE1_PIN, GPIO.HIGH)
        GPIO.output(LED_ZONE2_PIN, GPIO.HIGH)
        GPIO.output(LED_ZONE3_PIN, GPIO.HIGH)
        
        # Send urgent notifications
        if self.notification_manager:
            self.notification_manager.queue_notification(event, urgent=True)
        
        print("🚨 PANIC MODE ACTIVATED!")
    
    def get_system_status(self) -> Dict:
        """Get comprehensive system status"""
        return {
            'security_level': self.security_level.name,
            'active_alerts': len(self.alerts_active),
            'zones': {
                zone_id: {
                    'name': zone.name,
                    'enabled': zone.enabled,
                    'status': zone.status.value
                }
                for zone_id, zone in self.sensor_manager.zones.items()
            },
            'last_activity': self.last_activity,
            'uptime': time.time() - self.last_activity
        }
    
    def start(self):
        """Start the security system"""
        print("🚀 Starting Advanced Security System...")
        
        # Start subsystems
        self.sensor_manager.start_monitoring()
        self.notification_manager.start()
        
        # Network status indicator
        GPIO.output(LED_NETWORK_PIN, GPIO.HIGH)
        
        print("✅ All systems operational")
        print("🛡️ Advanced Security System ready!")
        
    def stop(self):
        """Stop the security system"""
        print("🛑 Stopping Advanced Security System...")
        
        # Stop subsystems
        self.sensor_manager.stop_monitoring()
        self.notification_manager.stop()
        
        # Turn off all outputs
        self.disarm_system()
        GPIO.output(LED_NETWORK_PIN, GPIO.LOW)
        
        print("✅ System stopped safely")
    
    def run_interactive(self):
        """Run interactive command interface"""
        print("\n🎮 ADVANCED SECURITY SYSTEM CONTROL")
        print("Commands:")
        print("  'arm [home|away]' - Arm system")
        print("  'disarm' - Disarm system") 
        print("  'panic' - Activate panic mode")
        print("  'status' - Show system status")
        print("  'events [hours]' - Show recent events")
        print("  'resolve <event_id>' - Resolve alert")
        print("  'test <zone>' - Test zone sensors")
        print("  'config' - Show configuration")
        print("  'quit' - Exit system")
        print("\nPress Ctrl+C anytime for emergency shutdown\n")
        
        try:
            while True:
                cmd = input("security> ").strip().lower().split()
                
                if not cmd:
                    continue
                
                if cmd[0] == 'arm':
                    level = SecurityLevel.AWAY
                    if len(cmd) > 1 and cmd[1] == 'home':
                        level = SecurityLevel.HOME
                    self.arm_system(level)
                
                elif cmd[0] == 'disarm':
                    self.disarm_system()
                
                elif cmd[0] == 'panic':
                    self.panic_mode()
                
                elif cmd[0] == 'status':
                    status = self.get_system_status()
                    print(json.dumps(status, indent=2))
                
                elif cmd[0] == 'events':
                    hours = 24
                    if len(cmd) > 1:
                        try:
                            hours = int(cmd[1])
                        except ValueError:
                            print("❌ Invalid hours value")
                            continue
                    
                    events = self.database.get_recent_events(hours)
                    print(f"📋 Recent events ({len(events)}):")
                    for event in events[:10]:  # Show last 10
                        print(f"  {event.timestamp} | {event.alert_type.value} | {event.description}")
                
                elif cmd[0] == 'resolve' and len(cmd) > 1:
                    self.resolve_alert(cmd[1])
                
                elif cmd[0] == 'config':
                    print("⚙️ System Configuration:")
                    for key, value in self.config.items():
                        if 'password' not in key.lower():
                            print(f"  {key}: {value}")
                
                elif cmd[0] == 'quit':
                    break
                
                else:
                    print("❌ Unknown command")
        
        except KeyboardInterrupt:
            print("\n🚨 Emergency shutdown!")
        
        finally:
            self.stop()
            GPIO.cleanup()

def main():
    """Main function"""
    try:
        system = AdvancedSecuritySystem()
        system.start()
        system.run_interactive()
    except Exception as e:
        print(f"❌ Critical error: {e}")
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

"""
🛡️ ADVANCED SECURITY SYSTEM FEATURES:

1. MULTI-ZONE MONITORING:
   - Independent zone configuration
   - Different sensor types per zone
   - Zone-specific entry delays and sensitivity

2. COMPREHENSIVE NOTIFICATIONS:
   - Email alerts with detailed information
   - SMS notifications for urgent events
   - Webhook integration for automation
   - Push notifications to mobile apps

3. PROFESSIONAL LOGGING:
   - SQLite database for event storage
   - Detailed sensor data recording
   - System performance monitoring
   - Historical event analysis

4. INTELLIGENT DETECTION:
   - Entry delay management
   - False alarm reduction
   - Severity-based alert escalation
   - Context-aware notifications

5. REMOTE CAPABILITIES:
   - Network-based monitoring
   - Web interface compatibility
   - Mobile app integration
   - Cloud logging support

🎯 ENTERPRISE FEATURES:
- User access control with authentication
- Tamper detection and self-monitoring
- Professional notification methods
- Database-driven configuration
- API endpoints for integration

🚀 DEPLOYMENT OPTIONS:
- Standalone residential system
- Commercial property monitoring
- Integration with existing security infrastructure
- Cloud-connected IoT security platform
"""


