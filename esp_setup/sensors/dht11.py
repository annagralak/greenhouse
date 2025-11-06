import dht 

from .sensor_template import Sensor
from machine import Pin
from time import sleep

class DHT11Sensor(Sensor):
    def __init__(self, name:str, pin: int):
        super().__init__(name)
        self.sensor = dht.DHT11(Pin(pin))

    def read(self) -> dict:
        super().read()    
    
        try:
            self.sensor.measure()
            return {
                "timestamp": self.timestamp,
                "temperature": self.sensor.temperature(),
                "humidity": self.sensor.humidity(),
            }
        except Exception as e:
            # return error info (still with timestamp)
            return {
                "timestamp": self.timestamp,
                "error": str(e)}
            
