#!/usr/bin/env python3
"""
Simple setup test.
- Tries to import RPi.GPIO (only works on a Raspberry Pi)
- Prints friendly messages so beginners know what to do next
"""

def main() -> None:
    print("👋 Hello! Let's test your Raspberry Pi setup.")
    try:
        import RPi.GPIO as GPIO  # type: ignore
        print("✅ RPi.GPIO is installed!")
        print("🎉 You're ready to run the sensor projects on your Raspberry Pi.")
    except Exception as exc:  # noqa: BLE001
        print("⚠️ Could not import RPi.GPIO.")
        print("This is normal if you're not running on a Raspberry Pi right now.")
        print("On your Pi, run: sudo apt install python3-gpiozero -y && pip3 install RPi.GPIO")
        print(f"Extra info: {exc}")

if __name__ == "__main__":
    main()


