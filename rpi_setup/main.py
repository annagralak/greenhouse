# import paho.mqtt.client as mqtt
import argparse

from logger import Logger
from mqtt_client import MQTTClient
from rules import RuleEngine
from relay_controller import RelayController
from state import StateStore
from utils import load_config, load_rules_from_config

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

	relay_config = config.get("relays", [])

	relay = RelayController(relay_config)
	state = StateStore()
	engine = RuleEngine(state, relay)

	userdata = {
        "state": state,
    	"engine": engine,
        "broker": config["mqtt_broker"],
        "port": config.get("mqtt_port", 1883),
        "topics": config.get("topic_list", [])
    }

	rules = load_rules_from_config(config, state, relay)

	for rule in rules:
		engine.add_rule(rule)

	mqtt_client = MQTTClient(state, engine, logger, config)
    
	print("Starting MQTT subscriber...")
	mqtt_client.connect()
	mqtt_client.loop_forever()

