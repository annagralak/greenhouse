from datetime import datetime
import time
import board
import adafruit_dht

# The data pin is connected to GPIO 4
GPIO = board.D4
# Time interval between next measurements in seconds
TIME_INTERVAL = 10 

def measure_temp_and_humidity():
	now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
	try:
		temperature = sensor.temperature
		humidity = sensor.humidity
		print(f"Temperature: {temperature}ºC, "
			f"Humidity: {humidity}%, Date: {now}")
		return temperature, humidity
	 
	except RuntimeError as error:
		print(f"RuntimeError: {error.args[0]}")
		time.sleep(2.0)
		# RuntimeError is expected from time to time, so just
		# recursively try again
		measure_temp_and_humidity()
        
	except Exception as error:
		# Stop when it is a new problem
		sensor.exit()
		raise error
    
if __name__ == "__main__":
	# Sensor type is DHT11
	sensor = adafruit_dht.DHT11(GPIO)
	
	while True:
		measure_temp_and_humidity()
		time.sleep(TIME_INTERVAL)
