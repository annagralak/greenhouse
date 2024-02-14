import time
import board 
import digitalio

# GPIO pin setup 
LIGHT_SENSOR = board.D26
LED = board.D16

def local_setup():
	light = digitalio.DigitalInOut(LIGHT_SENSOR)
	
	led = digitalio.DigitalInOut(LED)
	led.direction = digitalio.Direction.OUTPUT
	
	return led, light
	
def light_setup(is_dark, led):
	"""
	This function sets the lighting depending on the photoresistor state.
	"""
	# Light sensor will return 1 if it is dark outside

	if(is_dark):
		led.value = True
	else:
		led.value = False
	return led

if __name__ == "__main__":
	led, light = local_setup()
	
	while(True):
		led = light_setup(light.value, led)
		time.sleep(1)
