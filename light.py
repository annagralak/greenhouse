import time
import board 
import digitalio

# GPIO pin setup 
LIGHT_SENSOR_PIN = 26
LED_PIN = 16

# to do it better later
PIN_MAPPING = {
	16: board.D16,
	26 : board.D26
	}

class LightSensor:
	"""
	A class used for the GRL-12503 light sensor.

	Attributes
	----------
	sensor_pin : int
		GPIO pin for the sensor data

	light_sensor : board obj
		The object for the LED pin
        1 if there is less light outside than the limit level
        0 if there is more light outside that the limit level
        Note: Limit level should be set by the potetntiometer on the device	

	Methods
    -------
    read_value()
        Returns the status of the light sensor

    Raises
    -------
    TODO

	"""

	def __init__(self, sensor_pin):
	
		self.sensor_pin = sensor_pin
		self.light_sensor = digitalio.DigitalInOut(PIN_MAPPING[self.sensor_pin])

		
	def read_value(self):
		# Light sensor will return 1 if it is dark outside
		return self.light_sensor.value


class GreenhouseLed():
	"""
	A class used for controling the LED light in the greenhouse

	Attributes
	----------
	led_pin : int
		GPIO pin for the led lightening
	led: board obj
		The object for a led pin

	Methods
    -------
    light_setup(sensor_status)
        Will turn on or off the lighting basing on light sensor status

    Raises
    -------
    TODO
    
	"""

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

	light_sensor = LightSensor(LED_PIN)
	greenhouse_led = GreenhouseLed(LIGHT_SENSOR_PIN)	

	while True: 
		greenhouse_light.light_setup(light_sensor.read_value())
		time.sleep(1)