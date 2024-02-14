from datetime import datetime
import time
import board
import adafruit_dht

# Time interval between next measurements in seconds
TIME_INTERVAL = 10 

# The data pin is connected to GPIO 4
TEMP = board.D4

def local_setup():
	# Sensor type is DHT11
	sensor = adafruit_dht.DHT11(TEMP)
	return sensor

def measure_temp_and_humidity(sensor): 
	try:
		temperature = sensor.temperature
		humidity = sensor.humidity
		return temperature, humidity
	 
	except RuntimeError as error:
		print(f"RuntimeError: {error.args[0]}")
		time.sleep(2.0)
		# RuntimeError is expected from time to time, so just
		# recursively try again
		temperature, humidity = measure_temp_and_humidity(sensor)
		return temperature, humidity
        
	except Exception as error:
		# Stop when it is a new problem
		sensor.exit()
		raise error
    
if __name__ == "__main__":
	sensor = local_setup()
	
	while True:
		temp, humidity = measure_temp_and_humidity(sensor)
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(f"Temperature: {temp}ºC, "
			f"Humidity: {humidity}%, Date: {now}")
		time.sleep(TIME_INTERVAL)
