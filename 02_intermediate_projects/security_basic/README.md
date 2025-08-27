# 🛡️ Basic Security System

**Intermediate Level** | **Estimated Time: 2-3 hours** | **Difficulty: ⭐⭐⭐**

Build a real security system that detects intruders and logs everything! This project teaches you about sensors, event handling, data logging, and building practical security applications.

## 🎬 What It Does

Your security system will:
- **Detect intrusions** using IR break-beam sensors
- **ARM/DISARM** with physical buttons
- **Sound alarms** with buzzer and flashing LEDs
- **Log all events** with timestamps to a file
- **Entry delays** to allow time to disarm
- **Smart debouncing** to prevent false alarms

## 🛠️ What You'll Need

### Hardware Components
- **Raspberry Pi 5** with GPIO pins
- **1x IR Break-Beam Sensor** (transmitter + receiver)
- **1x Active Buzzer Module** for audio alerts
- **3x LEDs** (Green=Armed, Red=Alert, Blue=Status)
- **2x Push Buttons** (ARM and DISARM)
- **3x 220Ω Resistors** for LEDs
- **2x 10kΩ Resistors** for button pull-ups
- **Breadboard** and **jumper wires**

### Software
- **Python 3** with RPi.GPIO library
- **JSON** for event logging
- **datetime** for timestamps

## 🔌 Wiring Diagram

```
Raspberry Pi 5 Connections:
┌─────────────────────────────────────┐
│ Component           │ Pi Pin │ GPIO │
├─────────────────────────────────────┤
│ IR Sensor OUT       │   11   │ 17   │
│ Buzzer +            │   12   │ 18   │
│ LED Armed (Green)   │   16   │ 23   │
│ LED Alert (Red)     │   18   │ 24   │  
│ LED Status (Blue)   │   22   │ 25   │
│ Button ARM          │   3    │ 2    │
│ Button DISARM       │   5    │ 3    │
│ 5V Power            │   2    │ 5V   │
│ Ground              │   6    │ GND  │
└─────────────────────────────────────┘
```

### LED Connections (repeat for each):
```
GPIO Pin ──── 220Ω Resistor ──── LED+ ──── LED- ──── GND
```

### Button Connections (repeat for each):
```
GPIO Pin ──── 10kΩ Resistor ──── 3.3V
     │
     └──── Button ──── GND
```

### IR Sensor:
```
Transmitter: 5V ──── +, GND ──── -
Receiver: 5V ──── +, GND ──── -, GPIO17 ──── OUT
```

## 🚀 Quick Start

### 1. Setup Hardware
```bash
# Enable GPIO interfaces
sudo raspi-config
# Interface Options → SPI → Enable
# Interface Options → I2C → Enable
# Reboot when prompted
```

### 2. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python libraries (usually pre-installed)
sudo apt install python3-pip -y
pip3 install RPi.GPIO
```

### 3. Run the Security System
```bash
cd 02_intermediate_projects/security_basic/
python3 security_basic.py
```

## 🎮 How to Use

### System Operation
1. **Start the program** - Run the Python script
2. **ARM the system** - Press the ARM button
3. **Exit delay** - You have 10 seconds to leave the area
4. **Trigger test** - Break the IR beam to test detection
5. **Entry delay** - 5 seconds to disarm before alert
6. **DISARM** - Press DISARM button to stop monitoring

### LED Status Indicators
- **Green LED** - System is ARMED and monitoring
- **Red LED** - ALERT! Intrusion detected (flashing)
- **Blue LED** - System heartbeat (double-flash every 2 seconds)

### Audio Feedback
- **3 quick beeps** - System armed successfully
- **2 long beeps** - System disarmed successfully  
- **Continuous beeping** - ALERT! Intrusion detected

## 📊 Event Logging

The system automatically logs all events to `security_log.json`:

```json
[
  {
    "timestamp": "2024-01-15T14:30:25.123456",
    "event_type": "SYSTEM",
    "description": "Security system ARMED",
    "sensor_state": true
  },
  {
    "timestamp": "2024-01-15T14:35:10.654321", 
    "event_type": "INTRUSION",
    "description": "Motion detected! Alert #1",
    "sensor_state": false
  }
]
```

## 🔧 Configuration & Tuning

### Timing Settings
Edit these values in the code to customize behavior:

```python
self.config = {
    "alert_duration": 10,     # How long alerts last (seconds)
    "entry_delay": 5,         # Time to disarm before alert
    "exit_delay": 10,         # Time to leave after arming
    "sensitivity": 0.2        # Debounce time (seconds)
}
```

### Common Adjustments

**For office/home use:**
```python
"alert_duration": 30,    # Longer alerts
"entry_delay": 10,       # More time to disarm
"exit_delay": 15,        # More time to leave
```

**For high-security areas:**
```python
"alert_duration": 60,    # Very long alerts
"entry_delay": 2,        # Quick trigger
"exit_delay": 5,         # Quick exit
```

## 🔧 Troubleshooting

### Common Issues

**System won't arm:**
- Check button wiring and pull-up resistors
- Verify button GPIO pins (2 and 3)
- Test buttons with multimeter

**False alarms:**
- Increase sensitivity value for more debouncing
- Check IR sensor alignment
- Shield sensor from environmental interference

**No sound alerts:**
- Verify buzzer is "active" type (has internal oscillator)
- Check 5V power connection to buzzer
- Test buzzer with direct 5V connection

**LEDs don't work:**
- Check resistor values (220Ω for 3.3V GPIO)
- Verify LED polarity (long leg = positive)
- Test LEDs with multimeter in diode mode

**Log file errors:**
- Check file permissions in directory
- Ensure sufficient disk space
- Verify Python can write to current directory

### Performance Tips

**Reduce false triggers:**
- Position IR beam away from air vents
- Use beam heights that avoid pets
- Add physical barriers around sensors

**Improve reliability:**
- Use shielded cables for long sensor runs
- Add capacitors across power connections
- Keep sensor lenses clean

## 🎯 Understanding the Code

### Key Programming Concepts

**Object-Oriented Design:**
```python
class SecuritySystem:
    def __init__(self):
        # Initialize system state
    
    def arm_system(self):
        # Handle arming logic
```

**Event-Driven Programming:**
```python
def check_sensor(self):
    current_state = GPIO.input(IR_SENSOR_PIN)
    if self.last_sensor_state != current_state:
        # State changed - handle event
```

**Data Persistence:**
```python
def save_events(self):
    with open(self.log_file, 'w') as f:
        json.dump(events_dict, f, indent=2)
```

**State Management:**
```python
self.armed = False          # System armed state
self.alert_active = False   # Alert in progress
self.entry_delay_start = None  # Entry delay timing
```

## 🚀 Enhancement Ideas

### Beginner Modifications
- **SMS notifications** - Send text messages on alerts
- **Time-based arming** - Automatically arm/disarm on schedule
- **Multiple zones** - Different sensors for different areas
- **Web dashboard** - View logs and status remotely

### Advanced Upgrades
- **Camera integration** - Take photos during alerts
- **Machine learning** - Distinguish between people and pets
- **Network connectivity** - Remote monitoring and control
- **Mobile app** - Control system from smartphone
- **Home automation** - Integrate with smart home systems

### Professional Features
- **Backup power** - Battery backup for power outages
- **Tamper detection** - Alert if system is tampered with
- **Multiple users** - Different access codes for different people
- **Professional monitoring** - Send alerts to security company

## 🔬 Learning Objectives

After completing this project, you'll understand:
- **GPIO input/output** programming
- **Event-driven system design**
- **State management** in real-time systems
- **Data logging and persistence**
- **Debouncing and signal processing**
- **Real-world security system concepts**

## ⚠️ Security Considerations

**Important Notes:**
- This is a **learning project**, not a replacement for professional security
- **Test thoroughly** before depending on it
- **Backup power** recommended for critical applications
- **Multiple sensors** improve reliability
- **Regular maintenance** keeps system working properly

## 🎉 What's Next?

Ready for more advanced projects? Try:
- **[Advanced Security System](../../03_advanced_projects/security_advanced/)** - Multi-sensor system with network features
- **[Laser Light Show](../../03_advanced_projects/laser_show/)** - Create artistic patterns with precise control
- **[Light Follower](../light_follower/)** - Combine sensors with servo motors

---

*Congratulations on building your own security system! You've learned valuable skills in sensors, programming, and system design. Keep building and improving! 🚀*


