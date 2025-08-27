# 🎯 Light-Following Laser Project

**Intermediate Level** | **Estimated Time: 2-3 hours** | **Difficulty: ⭐⭐⭐**

Build an amazing laser system that automatically tracks and follows light sources! Point a flashlight around and watch the laser pointer follow it like a robotic pet. 🤖

## 🎬 What It Does

Your laser will:
- **Track moving lights** - Follow a flashlight beam around the room
- **Automatically adjust** - Constantly moves to point toward the brightest light
- **Smooth movement** - Uses servo motors for precise, fluid motion
- **Real-time feedback** - Shows sensor readings and positions on screen

## 🛠️ What You'll Need

### Hardware Components
- **Raspberry Pi 5** with GPIO pins
- **2x Servo Motors** (SG90 or similar) for X/Y movement
- **1x Laser Pointer Module** (KY-008 or similar)
- **4x Photoresistors (LDR)** for light detection
- **4x 10kΩ Resistors** for LDR circuits
- **4x 1µF Capacitors** for RC timing
- **Breadboard** and **jumper wires**
- **Mounting materials** (cardboard, 3D printed parts, etc.)

### Tools
- Screwdriver for servo mounting
- Hot glue gun or double-sided tape
- Wire strippers

## 🔌 Wiring Diagram

```
Raspberry Pi 5 Connections:
┌─────────────────────────────────────┐
│ Component        │ Pi Pin │ GPIO   │
├─────────────────────────────────────┤
│ Laser Module +   │   12   │ GPIO18 │
│ Laser Module -   │   6    │ GND    │
│ Servo X Signal   │   32   │ GPIO12 │
│ Servo Y Signal   │   33   │ GPIO13 │
│ Servo Power +    │   4    │ 5V     │
│ Servo Power -    │   6    │ GND    │
│ LDR Left         │   40   │ GPIO21 │
│ LDR Right        │   38   │ GPIO20 │
│ LDR Up           │   36   │ GPIO16 │
│ LDR Down         │   35   │ GPIO19 │
└─────────────────────────────────────┘
```

### LDR Circuit (Repeat for each sensor):
```
GPIO Pin ──── 10kΩ Resistor ──── LDR ──── GND
      │                           │
      └──── 1µF Capacitor ────────┘
```

## 🏗️ Physical Setup

### 1. Servo Mount Assembly
```
     [Laser Pointer]
           │
    ┌──────┴──────┐
    │  Y-Servo    │  (Vertical movement)
    │   (Tilt)    │
    └──────┬──────┘
           │
    ┌──────┴──────┐
    │  X-Servo    │  (Horizontal movement) 
    │   (Pan)     │
    └─────────────┘
```

### 2. Sensor Placement
Position the four LDRs around the laser mount:
- **Left sensor**: Points 45° left of laser direction
- **Right sensor**: Points 45° right of laser direction  
- **Up sensor**: Points 45° above laser direction
- **Down sensor**: Points 45° below laser direction

## 🚀 Quick Start

### 1. Setup Hardware
```bash
# Enable PWM and GPIO
sudo raspi-config
# Interface Options → SPI → Enable
# Interface Options → I2C → Enable
# Reboot when prompted
```

### 2. Install Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python GPIO library
sudo apt install python3-pip python3-gpiozero -y
pip3 install RPi.GPIO
```

### 3. Run the Project
```bash
cd 02_intermediate_projects/light_follower/
python3 light_follower.py
```

## 🎮 How to Use

1. **Start the program** - Run the Python script
2. **Wait for initialization** - Servos will move to center position
3. **Test with flashlight** - Shine a bright light around the sensors
4. **Watch it follow** - The laser should track your light source
5. **Press Ctrl+C** to stop safely

## 🔧 Tuning & Troubleshooting

### Common Issues

**Laser doesn't move smoothly:**
- Adjust `sensitivity` value (line 105) - lower = less aggressive
- Adjust `max_step` value (line 89) - lower = smoother movement

**Servos don't respond:**
- Check 5V power connection to servos
- Verify PWM pins are correct (GPIO12, GPIO13)
- Ensure servos are rated for 5V operation

**Sensors not detecting light:**
- Test individual LDR circuits with multimeter
- Check capacitor polarity and values
- Verify GPIO pins are correctly wired

**Erratic movement:**
- Add delays between readings
- Check for loose connections
- Shield sensors from laser reflection

### Performance Tuning

**For faster tracking:**
```python
sensitivity = 1.0      # More aggressive movement
max_step = 5.0        # Larger steps
time.sleep(0.05)      # Faster update rate
```

**For smoother tracking:**
```python
sensitivity = 0.2      # Gentler movement  
max_step = 1.0        # Smaller steps
time.sleep(0.2)       # Slower updates
```

## 🎯 Understanding the Code

### Key Concepts

**RC Timing Method:**
- Uses capacitor charge time to measure resistance
- Lower resistance (bright light) = faster charge = smaller time value
- Higher resistance (dim light) = slower charge = larger time value

**Servo Control:**
- PWM signals control servo position
- 2.5% duty cycle = 0° position
- 7.5% duty cycle = 90° position (center)
- 12.5% duty cycle = 180° position

**Tracking Algorithm:**
```python
# Compare horizontal sensors
horizontal_diff = left_reading - right_reading
if horizontal_diff > 0:
    # Right side is brighter, move right
    target_x = current_x + movement_amount
```

## 🚀 Enhancement Ideas

### Beginner Modifications
- **Add LED indicators** - Show which sensor detects brightest light
- **Sound effects** - Beep when tracking or losing target
- **Speed control** - Variable tracking speed with potentiometer

### Advanced Upgrades
- **Multiple target tracking** - Remember and cycle between light sources
- **Automatic calibration** - Self-adjust sensitivity based on environment
- **Remote control** - Manual override with wireless controller
- **Pattern mode** - Pre-programmed movement sequences
- **Camera integration** - Use Pi camera for visual tracking

## 🔬 Learning Objectives

After completing this project, you'll understand:
- **Servo motor control** with PWM signals
- **Analog sensor reading** using RC timing
- **Multi-sensor data fusion** for directional tracking
- **Real-time control systems** and feedback loops
- **Smooth motion algorithms** and position interpolation

## ⚠️ Safety Reminders

- **NEVER look directly into the laser beam** - Can damage eyes permanently
- **Keep laser power low** - Use only low-power (<5mW) laser pointers
- **Secure mounting** - Ensure servos and laser are firmly attached
- **Adult supervision** - Have an adult help with wiring and power connections
- **Work area safety** - Keep drinks and food away from electronics

## 🎉 What's Next?

Ready for more challenges? Try these projects:
- **[Basic Security System](../security_basic/)** - Use similar sensors for motion detection
- **[Advanced Security](../../03_advanced_projects/security_advanced/)** - Multi-sensor security with notifications
- **[Laser Light Show](../../03_advanced_projects/laser_show/)** - Create artistic laser patterns

---

*Have fun building your light-following laser! Remember: the best way to learn is by experimenting and making improvements! 🚀*


