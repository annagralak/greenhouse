import time
import datetime
import board
import adafruit_dht

from abc import ABC, abstractmethod

TEMP_PIN = board.D4


class Sensor(ABC):
    """
    A template class for all the sensors
    """
    @abstractmethod
    def read_data(self):
    	pass

class THSensor(adafruit_dht.DHT11, Sensor):
    """
    A class used for DHT11 temperature and humidity sensor.
    """

    def read_data(self): 
        now = datetime.datetime.now()
        timestamp = [now.date(), now.time()]

        try:
            return self.temperature, self.humidity, timestamp
		 
        except RuntimeError as error:
            print(f"RuntimeError: {error.args[0]}")

            time.sleep(2.0)
	        # RuntimeError is expected from time to time, so just recursively try again
            temperature, humidity = self.read_data()
            return temperature, humidity
	        
	# except Exception as error:
        # 	# Stop when it is a new problem
	# 	self.exit()
	# 	raise error

def TH_selftest():
    th_sensor = THSensor(TEMP_PIN)
	
    temp, humidity, datetime = th_sensor.read_data()

    print(f"Temperature: {temp}ºC, "f"Humidity: {humidity}%, Date: {datetime[0]}, Time: {datetime[1]}")


if __name__ == "__main__":
    TH_selftest()
