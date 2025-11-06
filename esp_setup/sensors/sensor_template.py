import utime

class Sensor:
    """
    Base class for all sensors.
    Subclasses must implement the read() method.
    """

    def __init__(self, name: str):
        self.name = name

    # This decorator doesn't work in MicroPython, but maybe tbd later
    #@abstractmethod
    def read(self) -> dict:
        """ 
        Return the sensor measurement as a dictionary.
        Must include at least 'timestamp'.
        Other keys might be sensor-specific.
        """
        self.timestamp = self.read_time()

    def read_time(self):
        t = utime.localtime()
        return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}".format(
        t[0], t[1], t[2], t[3], t[4]
    )

class DummyTempSensor(Sensor):
    def read(self):
        super().read()

        return {
            "timestamp": self.timestamp,
            "temperature": "25.3"
         }

if __name__ == "__main__":
    test_sensor = DummyTempSensor("DummyLivingRoomTemp")
    data = test_sensor.read()
    print(data) 
