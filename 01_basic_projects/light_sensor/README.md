# 💡 Project: Laser + LDR Tripwire (No ADC – RC Timing)
Use a handheld laser pointer and a photoresistor (LDR) to make a simple tripwire!

## 🎯 What This Project Does
- You shine a handheld laser pointer at a photoresistor (LDR).
- The Raspberry Pi measures how bright the light is using a timing trick.
- If the laser beam is blocked, it prints an alert.

This works without any extra chips (no ADC needed) by measuring how fast a capacitor charges through the LDR. Bright light = low resistance = fast charge. Dark = high resistance = slow charge.

## 🧠 What You'll Learn
- How an LDR changes resistance with light
- What an RC (resistor–capacitor) circuit is
- How to measure analog-ish values on the Pi using only digital GPIO

## 🧩 Parts You Need
- Raspberry Pi 5
- LDR (photoresistor)
- 10 kΩ resistor (brown-black-orange) – values from 10 kΩ to 100 kΩ work
- 1 µF capacitor (electrolytic or film; observe polarity if electrolytic)
- Jumper wires and a breadboard
- Handheld laser pointer

## ⚠️ Safety Notes
- Never point the laser at eyes. Use a wall or paper target.
- Double-check polarity on electrolytic capacitors (long leg = + to GPIO node).
- Only use 3.3V with GPIO. Never put 5V into a GPIO pin.

## 🔌 Wiring (RC Timing Method)
We’ll use GPIO 27 as the sense node.

Connections to the GPIO node (the same junction):
- LDR to 3.3V
- 10 kΩ resistor to GND
- 1 µF capacitor to GND
- Wire from this node to GPIO 27

In words: LDR pulls the node up toward 3.3V, resistor pulls it down to GND, capacitor goes from the node to GND. The Pi will discharge the capacitor, then let it charge and measure how long it takes to read HIGH.

Pin hints (physical header):
- 3.3V: Pin 1
- GND: Pin 6
- GPIO 27: Pin 13

## 🐍 Run the Code
```bash
cd 01_basic_projects/light_sensor
python3 ldr_tripwire.py
```

Follow the on-screen instructions: it will ask you to point the laser at the LDR for calibration. Then block the beam to trigger the alert.

## 🧪 Troubleshooting
- If readings don’t change: move the laser closer or build a paper tube around the LDR to block room light.
- If it always triggers: your threshold may be too low; rerun and make sure the laser is steady during calibration.
- If it never triggers: raise the threshold multiplier in the code, or try a larger resistor (e.g., 47 kΩ) for more sensitivity.

## 🌟 Upgrade Ideas
- Add an LED or buzzer alarm on another GPIO pin
- Save timestamps of trips to a log file
- Use two LDRs for direction sensing (which side was crossed first?)

Great job! This is a clever way to measure light without extra chips. 🚀


