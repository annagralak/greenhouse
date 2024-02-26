import time
import board 
import digitalio

# GPIO pin setup 
LIGHT_SENSOR = board.D26
LED = board.D16

class LightSensor:

	def __init__(self, sensor_pin):
		
		self.sensor_pin = sensor
		self.light = digitalio.DigitalInOut(self.sensor_pin)
		
		self.led_pin
		self.led = digitalio.DigitalInOut(self.led_pin)
		self.led.direction = digitalio.Direction.OUTPUT
		
	def read_value(self):
		
		# Light sensor will return 1 if it is dark outside
		return self.light.value


class GreenhouseLed():

	def __init__(self, led_pin):
				
		self.led_pin
		self.led = digitalio.DigitalInOut(self.led_pin)
		self.led.direction = digitalio.Direction.OUTPUT

	def light_setup(self, sensor_status):

		if(sensor_status):
			self.led.value = True
		else:
			self.led.value = False


if __name__ == "__main__":

	light_sensor = LightSensor(LED)
	greenhouse_led = GreenhouseLed(LIGHT_SENSOR)	

	while True: 
		status = light_sensor.read_value()
		greenhouse_light.light_setup(status)
		time.sleep(1)