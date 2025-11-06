import utime
import onewire
import ds18x20

from .sensor_template import Sensor
from machine import Pin

class DS18B20Sensor(Sensor):
    """
    DS18B20 temperature sensor.
    Returns temperature in Celsius from 1-Wire bus.
    """

    def __init__(self, name:str, pin: int):
        super().__init__(name)
        self.ds_pin = Pin(pin)
        self.ow = onewire.OneWire(self.ds_pin)
        self.ds = ds18x20.DS18X20(self.ow)
        self.roms = self.ds.scan()

        if not self.roms:
            raise Exception(f"No DS18B20 sensor found on pin {self.ds_pin}")

    def read(self) -> dict:
        super().read()    
    
        self.ds.convert_temp()
        # It needs some time to convert
        utime.sleep_ms(750)

        temps = []
        for rom in self.roms:
            temp_c = self.ds.read_temp(rom)
            temps.append(temp_c)

        return {
                "timestamp": self.timestamp,
                "temperature": temps[0] if len(temps) == 1 else temps
            }
            
