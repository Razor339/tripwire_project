# 🌟 Laser Light Show System

**Advanced Level** | **Estimated Time: 4-6 hours** | **Difficulty: ⭐⭐⭐⭐⭐**

Create your own professional-grade laser light show! This advanced project combines precision servo control, mathematical pattern generation, music synchronization, and interactive programming to create stunning visual displays.

## 🎬 What It Does

Your laser show system will:
- **Generate geometric patterns** - Circles, spirals, stars, and complex curves
- **Multi-color coordination** - Red, green, blue, and white laser combinations
- **Music synchronization** - React to audio beats and rhythm
- **Interactive control** - Real-time pattern switching and manual control
- **Pattern programming** - Create, save, and load custom patterns
- **Safety systems** - Emergency stops and position limiting

## 🛠️ What You'll Need

### Essential Hardware
- **Raspberry Pi 5** with GPIO expansion
- **2x High-precision Servo Motors** (MG90S or better)
- **1x Red Laser Module** (KY-008, <5mW)
- **2x Galvanometer Mirrors** (optional, for professional setup)
- **1x Emergency Stop Button** (large, red)
- **1x Audio Input Module** (for music sync)
- **Status LEDs** and **resistors**

### Optional Hardware (Multi-color)
- **1x Green Laser Module** (<5mW)
- **1x Blue Laser Module** (<5mW)
- **Beam combiners** and **dichroic mirrors**

### Mounting & Optics
- **Precision mounting brackets**
- **First-surface mirrors** (front-silvered)
- **Beam expanders** (optional)
- **Safety enclosure materials**

### Advanced Components
- **High-speed servos** (for professional shows)
- **ILDA interface** (for industry compatibility)
- **Smoke machine** (makes beams visible)

## 🔌 Wiring Diagram

```
Raspberry Pi 5 Connections:
┌─────────────────────────────────────┐
│ Component           │ Pi Pin │ GPIO │
├─────────────────────────────────────┤
│ Servo X (Pan)       │   32   │ 12   │
│ Servo Y (Tilt)      │   33   │ 13   │
│ Laser Red           │   12   │ 18   │
│ Laser Green         │   35   │ 19   │
│ Laser Blue          │   38   │ 20   │
│ Emergency Stop      │   40   │ 21   │
│ Status LED          │   36   │ 16   │
│ Audio Input         │   37   │ 26   │
│ 5V Power Bus        │   2,4  │ 5V   │
│ Ground Bus          │ 6,9,14 │ GND  │
└─────────────────────────────────────┘
```

### Servo Power Circuit
```
External 5V PSU ──┬── Servo 1 (Red wire)
                  ├── Servo 2 (Red wire)
                  └── Pi 5V Rail

Ground ───────────┬── Servo 1 (Brown wire)
                  ├── Servo 2 (Brown wire)
                  └── Pi Ground

GPIO 12 ────────────── Servo 1 Signal (Orange wire)
GPIO 13 ────────────── Servo 2 Signal (Orange wire)
```

### Laser Safety Circuit
```
GPIO 18 ──── 220Ω Resistor ──── Laser Red +
GPIO 19 ──── 220Ω Resistor ──── Laser Green +
GPIO 20 ──── 220Ω Resistor ──── Laser Blue +

Emergency Stop ──── Relay ──── Laser Power (Hardware cutoff)
```

## 🏗️ Mechanical Assembly

### Servo Mount Configuration
```
        [Laser Module]
             │
      ┌──────┴──────┐
      │ Y-Servo     │ ←── Vertical control (Tilt)
      │ (Mirror 2)  │
      └──────┬──────┘
             │
      ┌──────┴──────┐
      │ X-Servo     │ ←── Horizontal control (Pan)
      │ (Mirror 1)  │
      └─────────────┘
          Base Mount
```

### Mirror Positioning
- **First mirror** (X-servo): Controls horizontal sweep
- **Second mirror** (Y-servo): Controls vertical positioning
- **Mirror angle = Beam deflection × 2** (reflection law)
- Use **first-surface mirrors** for best beam quality

## 🚀 Quick Start

### 1. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python libraries
sudo apt install python3-pip python3-numpy -y
pip3 install RPi.GPIO numpy

# Install optional audio processing
pip3 install pyaudio scipy  # For advanced beat detection
```

### 2. Hardware Safety Check
```bash
# Test emergency stop
python3 -c "
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
print('Emergency stop:', 'PRESSED' if not GPIO.input(21) else 'RELEASED')
GPIO.cleanup()
"
```

### 3. Servo Calibration
```bash
# Test servo range and center positions
python3 -c "
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
servo = GPIO.PWM(12, 50)
servo.start(7.5)
time.sleep(2)
servo.stop()
GPIO.cleanup()
print('Servo should move to center position')
"
```

### 4. Run the Show
```bash
cd 03_advanced_projects/laser_show/
python3 laser_show.py
```

## 🎮 Interactive Commands

Once running, use these commands:

### Basic Control
```
laser> start circle          # Start circle pattern
laser> stop                  # Stop current show
laser> next                  # Switch to next pattern
laser> list                  # Show available patterns
```

### Advanced Control
```
laser> speed 2.5             # Set 2.5x speed
laser> music                 # Toggle music mode
laser> manual 90 45 red      # Manual position control
laser> save my_pattern.json  # Save current pattern
```

### Pattern Library
- **circle** - Perfect circles in various sizes
- **spiral** - Expanding/contracting spirals
- **figure_eight** - Infinity symbol patterns
- **star** - Multi-pointed star shapes
- **lissajous** - Mathematical curve patterns
- **rainbow_wave** - Color-cycling wave patterns

## 🎵 Music Synchronization

### Audio Input Setup
```bash
# Configure audio input device
arecord -l  # List audio devices
```

### Beat Detection Tuning
```python
# In laser_show.py, adjust these parameters:
beat_detector.beat_threshold = 0.1    # Minimum beat interval
beat_detector.sensitivity = 0.3       # Beat detection sensitivity
```

### Music Modes
- **Beat Flash** - Laser flashes white on beats
- **Color Change** - Changes colors on beats
- **Pattern Switch** - Switches patterns on beats
- **Speed Sync** - Adjusts speed to tempo

## 🔧 Advanced Configuration

### Servo Tuning
```python
# Adjust for your specific servos
def degrees_to_duty_cycle(self, degrees: float) -> float:
    # Standard servo: 2.5% = 0°, 12.5% = 180°
    # High-end servo: 1% = 0°, 11% = 180°
    return 2.5 + (degrees / 180.0) * 10.0  # Adjust multiplier
```

### Safety Limits
```python
# Prevent servo damage and unsafe beam directions
x = max(30, min(150, x))  # Limit horizontal range
y = max(30, min(150, y))  # Limit vertical range
```

### Performance Optimization
```python
# For faster patterns, reduce step delay
time.sleep(0.01 / speed)  # Adjust base delay

# For smoother movement, increase interpolation steps
steps = max(1, int(distance) // 1)  # More steps = smoother
```

## 📐 Creating Custom Patterns

### Mathematical Functions
```python
def custom_pattern(self):
    points = []
    for i in range(100):
        t = (i / 100) * 4 * math.pi
        
        # Your mathematical function here
        x = 90 + 30 * math.sin(t)
        y = 90 + 30 * math.cos(2 * t)
        
        points.append(LaserPoint(x, y, LaserColor.RED, 0.05))
    
    return Pattern("Custom", points)
```

### Interactive Pattern Recording
```python
# Record manual movements as patterns
def record_pattern(self):
    recorded_points = []
    # Move laser manually and record positions
    # Save as new pattern file
```

## 🔬 Advanced Features

### Professional ILDA Integration
```python
# Load ILDA standard laser show files
def load_ilda_file(filename):
    # Parse ILDA binary format
    # Convert to internal pattern format
```

### Network Control
```python
# Add HTTP API for remote control
from flask import Flask, request
app = Flask(__name__)

@app.route('/api/pattern/<name>')
def start_pattern(name):
    laser_show.start_show(name)
    return {'status': 'started', 'pattern': name}
```

### Multi-Projector Sync
```python
# Synchronize multiple laser projectors
class LaserNetwork:
    def __init__(self):
        self.projectors = []
    
    def sync_pattern(self, pattern, delay_offsets):
        # Start pattern on all projectors with timing offsets
```

## ⚠️ Critical Safety

### Laser Safety Classification
- **Class 1**: Safe under normal conditions (<0.39mW)
- **Class 2**: Visible laser, eye blink protection (<1mW) ⭐ **Recommended**
- **Class 3R**: May be hazardous (<5mW) ⚠️ **Use with caution**
- **Class 3B**: Definitely hazardous (5-500mW) ❌ **Not recommended**

### Safety Checklist
- [ ] **Laser power <5mW** - Verify with power meter
- [ ] **Emergency stop works** - Test before every use
- [ ] **Beam containment** - Audience protection barriers
- [ ] **Eye protection** - Safety goggles when adjusting
- [ ] **Warning signs** - "Laser in Use" signage
- [ ] **Trained operation** - Adult supervision required

### Hardware Safety Features
```python
def safety_check(self):
    # Implement these safety features:
    # 1. Emergency stop monitoring
    # 2. Servo position limits  
    # 3. Laser power monitoring
    # 4. Thermal protection
    # 5. Interlock systems
```

## 🎭 Show Ideas & Applications

### Educational Demonstrations
- **Geometry visualization** - Show mathematical concepts
- **Physics demonstrations** - Wave patterns and interference
- **Art installations** - Interactive artistic displays

### Entertainment Applications
- **DJ light shows** - Club and event lighting
- **Theater effects** - Stage and performance enhancement
- **Home parties** - Safe indoor entertainment

### Advanced Projects
- **Planetarium shows** - Astronomical visualization
- **Architectural projection** - Building facade displays
- **Scientific visualization** - Data representation

## 🚀 Enhancement Ideas

### Beginner Upgrades
- **Voice control** - "Start circle pattern"
- **Mobile app** - Smartphone remote control
- **Preset shows** - One-button complex sequences

### Advanced Modifications
- **3D projection** - Add Z-axis control with additional servos
- **Holographic effects** - Persistence of vision patterns
- **AI pattern generation** - Machine learning for unique patterns
- **VR integration** - Virtual reality pattern design

### Professional Features
- **DMX integration** - Professional lighting control
- **Timecode sync** - Frame-accurate synchronization
- **Color temperature control** - Artistic color mixing
- **Atmospheric integration** - Fog and haze coordination

## 🔬 Learning Objectives

After completing this project, you'll master:
- **Precision servo control** and PWM programming
- **Mathematical pattern generation** and trigonometry
- **Real-time system design** and threading
- **Audio signal processing** and beat detection
- **File I/O and data persistence** for pattern storage
- **Safety system implementation** and risk management
- **Professional laser show concepts** and industry standards

## 🎉 What's Next?

Ready for even more advanced projects?
- **[Advanced Security System](../security_advanced/)** - Multi-sensor integration
- **Build a laser harp** - Interactive musical instrument
- **Projection mapping** - Map patterns onto 3D surfaces
- **Laser communication** - Data transmission via laser

---

*Congratulations on building a professional laser show system! You've mastered advanced programming, precise hardware control, and safety engineering. Your skills are now ready for professional applications! 🌟*

**Remember: With great laser power comes great responsibility! Always prioritize safety! 🔒**


