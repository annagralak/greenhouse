import time 

class SensorValue:
    """Container for a single sensor reading."""

    def __init__(self, data: dict):
        """Store raw data and extract metadata fields."""

        self.data = data
        self.timestamp = data.get("timestamp")
        self.error = data.get("error")

class StateStore:
    """Holds latest sensor state and tracks updates."""

    def __init__(self):
        """Initialize state storage and change tracking."""

       # sensor_name -> SensorValue
        self._state = {}   
        self._changed = set()  
        
    def _now(self):
        """Return current time (YYYY-MM-DD HH:MM)."""

        return time.strftime("%Y-%m-%d %H:%M", time.localtime())

    def update_from_batch(self, batch: dict):
        """Update state from batch; normalize timestamp and track changes."""

        now = self._now()   

        for sensor_name, data in batch.items():

            # Normalize timestamp here
            if isinstance(data, dict):
                # Copy so the external object is not mutated
                data = dict(data)  

                # Add RPi time
                data["timestamp"] = now  

            old = self._state.get(sensor_name)

            if old is None or old.data != data:
                self._state[sensor_name] = SensorValue(data)
                self._changed.add(sensor_name)

    def get(self, sensor_name):
        """Return full sensor data or None."""

        obj = self._state.get(sensor_name)
        return obj.data if obj else None

    def get_value(self, sensor_name):
        """Return 'value' field or None."""

        obj = self._state.get(sensor_name)
        if not obj:
            return None
        return obj.data.get("value")

    def snapshot(self):
        """Return full state as dict."""

        return {
            k: v.data for k, v in self._state.items()
        }

    def get_changed(self):
        """Return list of changed sensors without clearing."""
        return list(self._changed)


    def clear_changed(self):
        """Reset change tracking."""
        self._changed.clear()
