from .sensor_template import Sensor
from .lib.bme280_float import BME280
from machine import I2C, Pin

class BME280Sensor(Sensor):
    """
    BME280 sensor for temperature, pressure and humidity.
    """

    def __init__(self, name:str, i2c_scl:int, i2c_sda:int):
        super().__init__(name)
        
        i2c_addr = 0x76
        self.i2c = I2C(0, scl=Pin(i2c_scl), sda=Pin(i2c_sda))
        self.sensor = BME280(i2c=self.i2c, addr=i2c_addr)

    def read(self) -> dict:
        super().read()    
        
        temp, pres, hum = self.sensor.read_compensated_data()
        
        # bme280_float already returns this
        # Convert to human-readable units
        #temperature = temp / 100 # °C
        #pressure = pres / 25600 # hPa
        #humidity = hum / 1024 # %

        return {
            "timestamp": self.timestamp,
            "temperature": temp,
            "pressure": pres, 
            "humidity": hum
        } 
