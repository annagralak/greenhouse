# import paho.mqtt.client as mqtt
import argparse
import time

from gpiozero import Device
from gpiozero.pins.pigpio import PiGPIOFactory

# Use pigpio hardware-timed GPIO backend for stable servo control
Device.pin_factory = PiGPIOFactory()

from logger import Logger
from mqtt_client import MQTTClient
from rules import RuleEngine
from device_controller import DeviceController
from state import StateStore
from utils import load_config


CONFIG_FILE = "config.json"

if __name__ == "__main__":
	
	config = load_config(CONFIG_FILE)
	if not config:
		exit(1)

	parser = argparse.ArgumentParser()
	parser.add_argument("-o", "--output", help="Optional filename for output")
	args = parser.parse_args() 

	base_filename = args.output if args.output else "data"
	logger = Logger(base_filename=base_filename, folder="data")

	device_config = config.get("devices", [])
	
	state = StateStore()
	device_controller = DeviceController(device_config, state)
	rule_engine = RuleEngine(state)

	rule_engine.load_from_config(config)

	mqtt_client = MQTTClient(state, logger, config)
    
	print("Starting MQTT subscriber...")
	mqtt_client.connect()

	try:
		while True:
			# Process MQTT messages
			mqtt_client.loop()

			# Rule engine only updates state
			rule_engine.evaluate_time_rules()

			if state.get_sensors_changed():
				rule_engine.evaluate_sensor_rules()

			# Apply state changes to hardware
			device_controller.apply()

			time.sleep(1)

	except KeyboardInterrupt:
		print("Keyboard interruption")

	finally:
		print("Shutting down safely...")

		device_controller.shutdown()

		mqtt_client.disconnect() 
	    

