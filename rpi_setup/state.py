import time 

class StateStore:
    """Central state manager for sensors and devices."""

    def __init__(self):
        """Initialize state storage and change tracking."""

        # Sensor state
        self._sensors = {} # sensor_name -> SensorValue
        self._sensors_changed = set()  

        # Device state
        self._devices = {}
        self._devices_changed = set()

    def _now(self):
        """Return current time (YYYY-MM-DD HH:MM)."""

        return time.strftime("%Y-%m-%d %H:%M", time.localtime())

    # =========================================================
    # SENSOR API
    # =========================================================

    def update_from_batch(self, batch: dict):
        """Update sensor state from batch, normalize timestamp and track changes."""

        now = self._now()   

        for sensor_name, data in batch.items():

            # Normalize timestamp here
            if isinstance(data, dict):
                # Copy so the external object is not mutated
                data = dict(data)  

                # Overwrite ESP32 timestamp with RPi time
                data["timestamp"] = now  

            old = self._sensors.get(sensor_name)

            if old is None or old.data != data:
                self._sensors[sensor_name] = SensorValue(data)
                self._sensors_changed.add(sensor_name)

            # TODO - add alert here if difference is too big?

    def get_sensor(self, sensor_name):
        """Return full sensor data."""

        obj = self._sensors.get(sensor_name)
        return obj.data if obj else None

    def get_sensor_value(self, sensor_name):
        """Return 'value' field or None."""

        obj = self._sensors.get(sensor_name)
        return obj.data.get("value") if obj else None

    def sensor_snapshot(self):
        """Return snapshot of all sensor states."""

        return {
            k: v.data for k, v in self._sensors.items()
        }

    def get_sensors_changed(self):
        """Return sensors that changed since last evaluation."""
        return list(self._sensors_changed)

    def clear_sensor_changes(self):
        """Reset change tracking."""
        self._sensors_changed.clear()

    # =========================================================
    # DEVICE API
    # =========================================================

    def set_device_state(self, device_id, data: dict):
        """Set desired device state and mark device as changed if needed."""

        now = self._now()

        if not isinstance(data, dict):
            data = {"value": data}

        value = data.get("value")

        old = self._devices.get(device_id)
        old_value = old.data.get("value") if old else None

        if old_value == value:
            return  # no change → no noise

        self._devices[device_id] = DeviceValue({
            "value": value,
            "timestamp": now
        })

        self._devices_changed.add(device_id)

    def get_device(self, device_id):
        """Return full device state."""
        
        obj = self._devices.get(device_id)
        return obj.data if obj else None

    def device_snapshot(self):
        """Return all device states."""
        
        return {k: v.data for k, v in self._devices.items()}

    def get_device_changed(self):
        """Return devices that changed since last apply cycle."""
        
        return list(self._devices_changed)

    def clear_device_changed(self):
        """Reset device change tracking."""
        
        self._devices_changed.clear()

    # =========================================================
    # DEBUG
    # =========================================================
    def debug_print(self):
        """Print current sensor and device state for debugging."""
        
        print("\n[SENSORS]")
        for name, data in self._sensors.items():
            print(f"{name}: {data.data}")

        print("\n[DEVICES]")
        for name, data in self._devices.items():
            print(f"{name}: {data.data}")

class SensorValue:
    """Container for a single sensor reading."""

    def __init__(self, data: dict):
        """Store raw data and extract metadata fields."""

        self.data = data
        self.timestamp = data.get("timestamp")

class DeviceValue:
    """Current desired state of the device."""

    def __init__(self, data: dict):
        self.data = data
        self.timestamp = data.get("timestamp")


