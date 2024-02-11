import RPi.GPIO as GPIO    
import time

# GPIO pin setup 
LIGHT_SENSOR = 26
LED = 16

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LIGHT_SENSOR, GPIO.IN)
	GPIO.setup(LED, GPIO.OUT) 

def light(is_dark):
	"""
	This function sets the lighting depending on the photoresistor state.
	"""
	if(is_dark):
		GPIO.output(LED, GPIO.HIGH)
	else:
		GPIO.output(LED, GPIO.LOW)

if __name__ == "__main__":
	setup()
	
	while(True):
		# Light sensor will return 1 if it is dark outside
		is_dark = GPIO.input(LIGHT_SENSOR) 
		light(is_dark)
		time.sleep(1)
