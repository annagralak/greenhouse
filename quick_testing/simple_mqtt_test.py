from umqtt.simple import MQTTClient
import time

BROKER = "192.168.8.51"   # your RPi IP
CLIENT_ID = "esp32_test"

client = MQTTClient(CLIENT_ID, BROKER)

try:
    client.connect()
    print("Connected to MQTT broker")

    # Publish a test message
    client.publish(b"test/topic", b"hello from esp32")
    print("Message sent!")

    client.disconnect()
except Exception as e:
    print("Failed to connect or publish:", e)

