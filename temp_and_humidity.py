from datetime import datetime
import time
import board
import adafruit_dht

# Time interval between next measurements in seconds
TIME_INTERVAL = 10 

# Th)e data pin is connected to GPIO 4
TEMP_PIN = board.D4

class THSensor(adafruit_dht.DHT11)
	"""
	A class used for DHT11 temperature and humidity sensor

	Methods
    -------
    measure_temp_and_humidity()
        Returns self.temperature and self.humidity
	"""

	def measure_temp_and_humidity(): 
		try:
			return self.temperature, self.humidity
		 
		except RuntimeError as error:
			print(f"RuntimeError: {error.args[0]}")
			time.sleep(2.0)
			# RuntimeError is expected from time to time, so just
			# recursively try again
			temperature, humidity = self.measure_temp_and_humidity()
			return temperature, humidity
	        
		except Exception as error:
			# Stop when it is a new problem
			self.exit()
			raise error
    
if __name__ == "__main__":

	sensor = THSensor(TEMP_PIN)

	while True:		
		print(f"Temperature: {sensor.temperature}ºC, "
			f"Humidity: {sensor.humidity}%, Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

		time.sleep(TIME_INTERVAL)
