# 🚦 Project: IR Break-Beam Tripwire
Make a simple security "tripwire" that shouts when someone breaks the invisible beam!

## 🎯 What This Project Does
- You set up an invisible light beam using an IR (infrared) transmitter and receiver.
- When something passes through and breaks the beam, your Raspberry Pi detects it.
- The Pi prints a warning message (and you can add a buzzer or LED later!).

## 🧠 What You'll Learn
- How to wire an IR break-beam sensor pair
- How to read a digital sensor with a GPIO pin
- How to detect events (beam broken / beam restored) in Python

## 🧩 Parts You Need
- Raspberry Pi 5
- IR break-beam sensor pair (transmitter + receiver)
- Breadboard and jumper wires

Optional extras:
- LED + 330Ω resistor (for visual alarm)
- Piezo buzzer (for sound alarm)

## ⚠️ Safety Notes
- Keep wires neat and double-check connections before powering on.
- Never connect 5V directly to a Pi GPIO pin.
- If anything gets warm or smells funny, unplug power and check wiring.

## 🔌 Wiring Guide
We'll use 3.3V power to keep everything safe and simple.

Transmitter (usually 2 wires):
- VCC → 3.3V (Pin 1)
- GND → GND (Pin 6)

Receiver (usually 3 wires):
- VCC → 3.3V (Pin 1)
- GND → GND (Pin 6)
- OUT → GPIO 17 (Pin 11)

Tip: Point the transmitter directly at the receiver, a few inches apart to start.

How it works:
- When the beam is OK (not broken), the receiver output is usually HIGH.
- When the beam is BROKEN, the receiver output goes LOW.

We'll use the Pi's internal pull-up to keep the input HIGH unless the beam is broken.

## 🐍 Run the Code
```bash
cd 01_basic_projects/ir_sensor
python3 tripwire.py
```

- Break the beam with your hand: you should see "INTRUDER!" 😄
- Move your hand away: you should see "Beam restored."
- Press Ctrl+C to stop the program.

## 📄 Code Walkthrough (easy mode!)
Open `tripwire.py` and look for these parts:
- Setup: choose the pin and enable a pull-up resistor
- Events: functions that run when the beam is broken/restored
- Main loop: keeps the program running until you press Ctrl+C

## 🧪 Troubleshooting
- No messages? Make sure the transmitter LED is pointed at the receiver.
- Still nothing? Move them closer together.
- Reversed logic? Some sensors output the opposite. Swap the messages for HIGH/LOW.
- Random triggers? Try adding `bouncetime=200` (already in code) and tidy your wires.

## 🌟 Upgrade Ideas
- Add a buzzer on another pin and make it beep on intruder
- Log timestamps to a file when the beam is broken
- Trigger a camera picture when tripped

You built a real security sensor—nice work! 🚀


