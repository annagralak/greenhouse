import time
import board 
import digitalio
import adafruit_dht
from datetime import datetime
from light import LightSensor, GreenhouseLed
from temp_and_humidity import THSensor

# Time interval between next measurements in seconds
TIME_INTERVAL = 2

# GPIO pins 
LIGHT_SENSOR_PIN = board.D26
LED_PIN = board.D16
TH_SENSOR_PIN = board.D4


if __name__ == "__main__":

	th_sensor = THSensor(TEMP)

	light_sensor = LightSensor(LED_PIN)
	greenhouse_led = GreenhouseLed(LIGHT_SENSOR_PIN)	

	while True: 
		now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

		print("--------------------------")
		print(f"Time: {now}")

		temp, humidity = th_sensor.measure_temp_and_humidity()

		print(f"Temperature: {temp}ºC")
		print(f"Humidity: {humidity}%")

		greenhouse_light.light_setup(light_sensor.read_value())

		time.sleep(1)