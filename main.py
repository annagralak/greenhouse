import time
import board 
import digitalio
import adafruit_dht
from datetime import datetime
from light import LightSensor, GreenhouseLed
# from temp_and_humidity import measure_temp_and_humidity

# Time interval between next measurements in seconds
TIME_INTERVAL = 2

# GPIO pins 
LIGHT_SENSOR_PIN = board.D26
LED_PIN = board.D16
TH_SENSOR_PIN = board.D4


if __name__ == "__main__":

	light_sensor = LightSensor(LED_PIN)
	greenhouse_led = GreenhouseLed(LIGHT_SENSOR_PIN)	

	# temp and humidity sensor
	th_sensor = adafruit_dht.DHT11(TEMP)

	while True: 
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		print("--------------------------")
		print(f"Time: {now}")

		print(f"Temperature: {sensor.temperature}ºC")
		print(f"Humidity: {sensor.humidity}%")

		greenhouse_light.light_setup(light_sensor.read_value())

		time.sleep(1)