import RPi.GPIO as GPIO

class RelayController:
    """Manages GPIO relays defined in config."""

    def __init__(self, config, active_low=False):
        """Store relay config and initialize state cache."""
        
        self._state = {}
        # Some relays have inverted logic
        self._active_low = active_low

        self._relays = {
            r["id"]: r for r in config
        }

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        # Initialize all relay pins
        for relay_id, relay in self._relays.items():
            pin = relay["config"]["pin"]

            GPIO.setup(pin, GPIO.OUT)

            # ensure OFF state at startup
            self._write(pin, False)
            self._state[relay_id] = False
            print(f"[INIT] Relay {relay_id} (GPIO {pin}) -> OFF")

    def _write(self, pin, value):
        """Write raw GPIO level with optional active-low inversion."""
        if self._active_low:
            GPIO.output(pin, GPIO.LOW if value else GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.HIGH if value else GPIO.LOW)

    def set(self, relay_id, value):
        """Set relay state (avoid redundant updates)."""

        if self._state.get(relay_id) == value:
            return

        self._state[relay_id] = value

        pin = self._relays[relay_id]["config"]["pin"]

        self._write(pin, value)

        print(f"[RELAY] {relay_id} (GPIO {pin}) -> {value}")

    def shutdown(self):
        """Force all relays OFF before cleanup."""
        for relay_id, relay in self._relays.items():
            pin = relay["config"]["pin"]
            self._write(pin, False)
            print(f"[SHUTDOWN] Relay {relay_id} (GPIO {pin}) -> OFF")

    def cleanup(self):
        """Reset GPIO state safely."""
        self.shutdown()
        GPIO.cleanup()


# part below for testing
if __name__ == "__main__":
    import time

    TEST_PIN = 27

    relay_config = [
        {
            "id": "test_relay",
            "type": "gpio",
            "config": {
                "pin": TEST_PIN
            }
        }
    ]

    relay = RelayController(relay_config)

    print("Testing relay...")

    try:
        while True:
            relay.set("test_relay", True)
            time.sleep(2)

            relay.set("test_relay", False)
            time.sleep(2)

    except KeyboardInterrupt:
        print("Exiting...")
        relay.cleanup()