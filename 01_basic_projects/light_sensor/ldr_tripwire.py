#!/usr/bin/env python3
"""
💡 LDR TRIPWIRE (RC TIMING)

Uses a photoresistor (LDR), a resistor, and a capacitor to detect
when a handheld laser beam is blocked.

How it works:
- We DISCHARGE a capacitor by making the pin OUTPUT and LOW.
- We then switch the pin to INPUT and measure how long until it reads HIGH.
- Bright light (laser on LDR) → lower resistance → faster charge → smaller time.
- Dark (beam blocked) → higher resistance → slower charge → bigger time.
"""

import time
from typing import List

import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

SENSE_PIN = 27  # GPIO 27 (physical pin 13)

# Configure once; direction will change during measurement
GPIO.setup(SENSE_PIN, GPIO.OUT)


def discharge_capacitor(pin: int) -> None:
    """Force the capacitor to empty by pulling the node LOW for a short time."""
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    time.sleep(0.005)  # 5 ms is plenty for 1 µF with ~10 kΩ


def measure_charge_time(pin: int, timeout_s: float = 0.5) -> float:
    """Return milliseconds until the input reads HIGH, or timeout_ms if it never does."""
    discharge_capacitor(pin)
    GPIO.setup(pin, GPIO.IN)
    start = time.perf_counter()
    deadline = start + timeout_s
    while time.perf_counter() < deadline:
        if GPIO.input(pin) == GPIO.HIGH:
            elapsed = (time.perf_counter() - start) * 1000.0
            return elapsed
    # Timed out; return a large value so it clearly indicates "very dark"
    return timeout_s * 1000.0


def take_average_reading(samples: int = 5, delay_s: float = 0.02) -> float:
    """Average several charge-time readings to smooth out noise."""
    values: List[float] = []
    for _ in range(samples):
        values.append(measure_charge_time(SENSE_PIN))
        time.sleep(delay_s)
    return sum(values) / len(values)


def calibrate_baseline(num_samples: int = 20) -> float:
    """Ask the user to shine the laser on the LDR and compute a baseline time."""
    print("\n📏 Calibration: Point the laser steadily at the LDR and keep it still...")
    time.sleep(1.0)
    readings: List[float] = []
    for i in range(num_samples):
        value_ms = take_average_reading(samples=3)
        readings.append(value_ms)
        print(f"  Sample {i + 1}/{num_samples}: {value_ms:.1f} ms")
    baseline_ms = sum(readings) / len(readings)
    print(f"✅ Baseline (laser ON) ≈ {baseline_ms:.1f} ms")
    return baseline_ms


def main() -> None:
    try:
        baseline_ms = calibrate_baseline()
        # Threshold multiplier: values above this are considered "beam blocked"
        threshold_ms = max(baseline_ms * 1.8, baseline_ms + 20.0)
        restore_ms = threshold_ms * 0.85  # hysteresis to avoid chatter
        print(f"🚧 Trip threshold: > {threshold_ms:.1f} ms  (restore < {restore_ms:.1f} ms)")
        print("\nReady! Block the beam with your hand or paper to trigger.")

        tripped = False
        while True:
            value_ms = take_average_reading(samples=3)
            if not tripped and value_ms > threshold_ms:
                tripped = True
                print(f"\n🚨 TRIPPED! Charge time {value_ms:.1f} ms (beam blocked)")
            elif tripped and value_ms < restore_ms:
                tripped = False
                print(f"✅ Restored. Charge time {value_ms:.1f} ms (beam on)")
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\n🛑 Stopping LDR tripwire.")
    finally:
        GPIO.cleanup()
        print("✅ GPIO cleaned up.")


if __name__ == "__main__":
    main()


