from time import time

class SensorManager:
    """
    Manages multiple sensors.
    Calls each sensor's read() and aggregates results.
    """

    def __init__(self):
        self.sensors = []

    def add_sensor(self, sensor):
        """
        Add a sensor object (must inherit from Sensor) to the manager.
        """
        self.sensors.append(sensor)

    def read_all(self):
        """
        Read all sensors and return a dictionary.
        Structure:
        {
            "sensor_name_1": { ...data... },
            "sensor_name_2": { ...data... },
            ...
        }
        """
        all_data = {}
        for sensor in self.sensors:
            try:
                all_data[sensor.name] = sensor.read()
            except Exception as e:
                # handle sensor errors gracefully
                all_data[sensor.name] = {
                    "timestamp": time(),
                    "error": str(e)
                    }
        return all_data

# Testing below
if __name__ == "__main__":
    from sensor_template import Sensor

    class DummyTempSensor(Sensor):
        def read(self):
            return {"timestamp": self.read_time(), "temperature": 25.3}

    class DummyHumiditySensor(Sensor):
        def read(self):
            return {"timestamp": self.read_time(), "humidity": 40}

    manager = SensorManager()
    manager.add_sensor(DummyTempSensor("DummyTempLivingRoom"))
    manager.add_sensor(DummyHumiditySensor("DummyHumidityLivingRoom"))

    all_measurements = manager.read_all()
    for sensor_name, data in all_measurements.items():
        print(f"{sensor_name}: {data} ")

