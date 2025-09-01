import utime

from .sensor_template import Sensor
from machine import ADC, Pin

class CapacitiveMoistureSensor(Sensor):
    """
    Capacitive soil moisture sensor.
    Can read analog values from 0 (dry) to 4095 (wet)
    """

    def __init__(self, name:str, pin: int):
        super().__init__(name)

        self.adc_pin = ADC(Pin(pin))
        # Full range 0-3.3V
        self.adc_pin.atten(ADC.ATTN_11DB)
        # 0-4095
        self.adc_pin.width(ADC.WIDTH_12BIT)

    def read(self) -> dict:
        super().read()    
        
        moisture = self.adc_pin.read()
    
        return {
                "timestamp": self.timestamp,
                "moisture": moisture,
            }
            
