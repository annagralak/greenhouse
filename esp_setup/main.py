import time
import json

from umqtt.simple import MQTTClient
from wifi_manager  import WiFiManager
from sensors.sensor_manager import SensorManager
from sensors.dht11 import DHT11Sensor
from sensors.bme280 import BME280Sensor 
from sensors.ds18b20 import DS18B20Sensor
from sensors.hw103 import HW103Sensor
from sensors.capacitive_moisture import CapacitiveMoistureSensor

MQTT_BROKER = "192.168.4.1"
MQTT_PORT = 1883
MQTT_TOPIC = "greenhouse/esp32-1/sensors"

def main():
    # Connect to Wi-Fi
    wifi = WiFiManager()
    wifi.connect()

    # Setup SensorManager
    manager = SensorManager()

    # Add DHT11 sensor (define pin where it's connected, e.g. GPIO4)
    try:
        dht11 = DHT11Sensor(name="DHT11", pin=4)
        manager.add_sensor(dht11)
    except Exception as e:
        print(f"Sensor not added: {e}")
   
    try:
        bme280 = BME280Sensor(name="BME280", i2c_scl=22, i2c_sda=21)
        manager.add_sensor(bme280)
    except Exception as e:
        print(f"Sensor not added: {e}")

    try:
        ds18b20 = DS18B20Sensor(name="DS18B20", pin=15)
        manager.add_sensor(ds18b20)
    except Exception as e:
        print(f"Sensor not added: {e}")

# To be uncommented when tested better
#   
#    try:
#        hw103 = HW103Sensor(name="HW-103", pin=35)
#        manager.add_sensor(hw103)
#    except Exception as e:
#        print(f"Sensor not added: {e}")
#
#    try:
#        cap_moisture = CapacitiveMoistureSensor(name="Capacitive moisture", pin=34)
#        manager.add_sensor(cap_moisture)
#    except Exception as e:
#        print(f"Sensor not added: {e}")
#

    mqtt_client = MQTTClient("esp32_client", MQTT_BROKER, port = MQTT_PORT)
    mqtt_client.connect()    

    print("Setup complete. Starting loop...")

    # Main loop: read every 10 seconds
    while True:
        wifi.ensure_connected()  # keep Wi-Fi alive
        measurements = manager.read_all()
        payload = json.dumps(measurements)
        mqtt_client.publish(MQTT_TOPIC, payload)
         
        print(f"Published: {payload}")        
        time.sleep(600)

if __name__ == "__main__":
    main()

