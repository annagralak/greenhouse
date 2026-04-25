import json
import paho.mqtt.client as mqtt

from utils import pretty_print


class MQTTClient:
	"""MQTT handler connecting messages to state, logging, and rules."""

	def __init__(self, state_store, rule_engine, logger, config):
		"""Initialize MQTT client and callbacks."""
    
		self.state = state_store
		self.engine = rule_engine
		self.logger = logger
		self.config = config

		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message

	def on_connect(self, client, userdata, flags, rc):
		"""Subscribe to configured topics on connect."""

		print("Connected to broker")

		for topic in self.config["topic_list"]:
			client.subscribe(topic)
			print(f"Subscribed to topic: {topic}")

	def on_message(self, client, userdata, msg):
		"""Process incoming message: update state, log, evaluate rules."""

		payload = json.loads(msg.payload.decode())

		self.state.update_from_batch(payload)

		pretty_print(payload)
		self.logger.log(msg.topic, payload)

		changed_sensors = self.state.get_changed()

		if changed_sensors:
		    self.engine.evaluate(changed_sensors)
		    self.state.clear_changed()

	def connect(self):
		"""Connect to MQTT broker."""
	
		self.client.connect(
			self.config["mqtt_broker"],
			self.config.get("mqtt_port", 1883),
			60
		)

	def loop_forever(self):
		"""Start blocking MQTT loop."""
		
		self.client.loop_forever()
