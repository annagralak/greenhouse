import RPi.GPIO as GPIO
from gpiozero import AngularServo

class DeviceController:
    """Manages hardware devices and synchronizes them with system state."""
    
    def __init__(self, config, state_store, active_low=False):
        self.state = state_store
        self.devices = {}
        self.last_applied = {}
        self.active_low = active_low

        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        for d in config:
            device_id = d["id"]
            device_type = d["type"]
            pin = d["config"]["pin"]

            if device_type == "relay":
                self.devices[device_id] = RelayDriver(pin, active_low)

            elif device_type == "fan":
                self.devices[device_id] = FanDriver(pin)

            elif device_type == "servo":
                self.devices[device_id] = ServoDriver(
                    pin,
                    d["config"]["open"],
                    d["config"]["closed"]
                )

            else:
                raise ValueError(f"Unknown device type: {device_type}")

            # TODO - add this with default value from config
            # self.state.set_device_state(device_id, {"value": None})

            print(f"[INIT] {device_id} ({device_type}) on GPIO {pin}")      

    def apply(self):
        """
        Apply only changed device states from StateStore.
        No rule evaluation here.       
        """

        changed = self.state.get_device_changed()

        if not changed:
            return

        # What the system wants device to be
        snapshot = self.state.device_snapshot()

        for device_id in changed:

            desired = snapshot.get(device_id)
            if not desired:
                continue

            value = desired.get("value")

            # To avoid changing double
            if self.last_applied.get(device_id) == value:
                continue

            device = self.devices.get(device_id)
            if not device:
                continue

            # Hardware is updated here
            device.write(value)

            # Remember what was applied
            self.last_applied[device_id] = value

            print(f"[DEVICE] {device_id} -> {value}")

        self.state.clear_device_changed()


    def set(self, device_id, value):
        """Write desired state (does not touch hardware directly)."""
        
        self.state.set_device_state(device_id, value)

    def snapshot(self):
        """Return a summary of all initialized devices."""
        
        return {
            device_id: {
                "type": type(device).__name__,
                "repr": str(device)
            }
            for device_id, device in self.devices.items()
        }

    def shutdown(self):
        """Safely turn off all devices and release GPIO resources."""

        for device_id, device in self.devices.items():
            device.shutdown()
            print(f"[SHUTDOWN] {device_id}")

        GPIO.cleanup()

class RelayDriver:
    """GPIO relay driver for ON/OFF switching."""

    def __init__(self, pin, active_low=False):
        self.pin = pin
        self.active_low = active_low
        self.state = False

        GPIO.setup(pin, GPIO.OUT)
        self.write(False)

    def write(self, value: bool):
        """Set relay state ON or OFF."""

        if self.state == value:
            return

        self.state = value

        if self.active_low:
            GPIO.output(self.pin, GPIO.LOW if value else GPIO.HIGH)
        else:
            GPIO.output(self.pin, GPIO.HIGH if value else GPIO.LOW)

    def shutdown(self):
        """Turn relay OFF before shutdown."""

        self.write(False)
        GPIO.output(self.pin, GPIO.LOW)


class FanDriver:
    """Simple ON/OFF fan"""

    def __init__(self, pin):
        self.pin = pin
        self.state = False

        GPIO.setup(pin, GPIO.OUT)
        self.write(False)

    def write(self, value: bool):
        """Set fan state ON or OFF."""

        if self.state == value:
            return

        self.state = value
        GPIO.output(self.pin, GPIO.HIGH if value else GPIO.LOW)

    def shutdown(self):
        """Turn fan OFF before shutdown."""

        self.write(False)
        GPIO.output(self.pin, GPIO.LOW)

class ServoDriver:
    """Servo actuator with open/closed logical positions."""

    def __init__(self, pin, open, closed):
        self.pin = pin
        self.open = open
        self.closed = closed

        self.angle = self.closed

        self.servo = AngularServo(
            self.pin,
            min_angle=0,
            max_angle=180,
            min_pulse_width=0.0005,
            max_pulse_width=0.0025
        )

        # Start in closed position
        self.servo.angle =  self.closed

    def write(self, angle):
        """Move servo to defined angle """

        try:
            angle = float(angle)
        except (ValueError, TypeError):
            return

        # clamp to valid range (same as safety in standalone)
        angle = max(0, min(180, angle))

        # optional: avoid redundant writes (does NOT change behavior)
        if self.angle == angle:
            return

        self.angle = angle
        self.servo.angle = angle

    def shutdown(self):
        """Move servo to closed position and release control signal."""
        
        self.servo.angle = self.closed
        time.sleep(0.2)
        self.servo.angle = None

# Part below for testing
if __name__ == "__main__":

    import time
    from gpiozero import Device
    from gpiozero.pins.pigpio import PiGPIOFactory

    Device.pin_factory = PiGPIOFactory()
    
    from state import StateStore

    Device.pin_factory = PiGPIOFactory()

    device_config = [
        {
            "id": "test_relay_17",
            "type": "relay",
            "config": {
                "pin": 17
            }
        },
        {
            "id": "test_relay_27",
            "type": "relay",
            "config": {
                "pin": 27
            }
        },
        {
            "id": "test_servo",
            "type": "servo",
            "config": {
                "pin": 12
            }
        },
        {
          "id": "test_fan",
          "type": "fan",
          "config": {
            "pin": 22
          }
        },
    ]

    controller = DeviceController(device_config, StateStore())

    try:
        while True:

            print("Servo -> 0°")
            controller.set("test_servo", 0)
            controller.apply()
            time.sleep(3)

            print("Servo -> 90°")
            controller.set("test_servo", 90)
            controller.apply()
            time.sleep(3)

            # print("Servo -> 180°")
            # controller.set("test_servo", 180)
            # time.sleep(3)

            print("\nRelay 17 ON")
            controller.set("test_relay_17", True)
            controller.apply()
            time.sleep(2)

            print("Relay 17 OFF")
            controller.set("test_relay_17", False)
            controller.apply()
            time.sleep(2)

            print("\nRelay 27 ON")
            controller.set("test_relay_27", True)
            controller.apply()
            time.sleep(2)

            print("Relay 27 OFF")
            controller.set("test_relay_27", False)
            controller.apply()
            time.sleep(2)

            print("\nFan ON")
            controller.set("test_fan", True)
            controller.apply()
            time.sleep(2)

            print("Fan OFF")
            controller.set("test_fan", False)
            controller.apply()
            time.sleep(2)


    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        controller.shutdown()


