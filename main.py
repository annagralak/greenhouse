import time
import board 
import digitalio
import adafruit_dht
from datetime import datetime
from light import light_setup
from temp_and_humidity import measure_temp_and_humidity

# Time interval between next measurements in seconds
TIME_INTERVAL = 2

# GPIO pins 
LIGHT_SENSOR = board.D26
LED = board.D16
TEMP = board.D4

def setup():
	"""
 	This function will initialize all the settings such as GPIO pins
	""" 
	# Light
	light = digitalio.DigitalInOut(LIGHT_SENSOR)
	led = digitalio.DigitalInOut(LED)
	led.direction = digitalio.Direction.OUTPUT

	# Temperature and humidity
	sensor = adafruit_dht.DHT11(TEMP)
	return led, light, sensor

def main():
	led, light, sensor = setup()

	while True:
		led = light_setup(light.value, led)
		temp, humidity = measure_temp_and_humidity(sensor)
		# now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		print("--------------------------")
		print(f"Time: {now}")
		print(f"Temperature: {temp}ºC")
		print(f"Humidity: {humidity}%")
		print(f"Light status: {led.value}")

		time.sleep(TIME_INTERVAL)

if __name__ == "__main__":
	main()