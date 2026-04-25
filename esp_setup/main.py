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


CONFIG = "configs/sensor_config_esp32_zero.json"
DEFAULT_MQTT_PORT = 1883
DEFAULTT_TIME_INTERVAL = 60

SENSOR_TYPES = {
    "dht11": DHT11Sensor,
    "bme280": BME280Sensor,
    "ds18b20": DS18B20Sensor,
    "hw103": HW103Sensor,
    "capacitive": CapacitiveMoistureSensor, 
}

def load_config(path=CONFIG):
    try:
        with open(path, "r") as f:
            data = json.load(f)
    except Exception as e:
        print("Failed to load config:", e)
        return None

    print("Config data:")
    print(data)

    required = ["id", "mqtt_broker", "topic", "sensors"]
    for key in required:
        if key not in data:
            print("Missing config field:", key)
            return None

    # Defaults
    if "mqtt_port" not in data:
        data["mqtt_port"] = DEFAULT_MQTT_PORT

    if "loop_interval" not in data:
        data["loop_interval"] = DEFAULTT_TIME_INTERVAL

    return data

def create_sensor(sensor_cfg):
    sensor_type = sensor_cfg.get("type")
    sensor_id = sensor_cfg.get("id")
    config = sensor_cfg.get("config", {})

    cls = SENSOR_TYPES.get(sensor_type)
    if not cls:
        raise Exception("Unknown sensor type: " + str(sensor_type))

    return cls(name=sensor_id, **config)

def main():
    config = load_config()
    if not config:
        print("Invalid config. Stopping.")
        return

    wifi = WiFiManager()
    wifi.connect()

    mqtt_client = MQTTClient(
        config["id"],
        config["mqtt_broker"],
        port=config["mqtt_port"]
    )

    try:
        mqtt_client.connect()
    except Exception as e:
        print("MQTT connection failed:", e)
        return

    manager = SensorManager()

    for sensor_cfg in config["sensors"]:
        try:
            sensor = create_sensor(sensor_cfg)
            manager.add_sensor(sensor)
            print("Added sensor:", sensor_cfg.get("id"))
        except Exception as e:
            print("Sensor not added:", e)

    print("Setup complete. Starting loop...")
    while True:
        wifi.ensure_connected()  # keep Wi-Fi alive

        measurements = manager.read_all() 
        payload = json.dumps(measurements)

        mqtt_client.publish(config["topic"], payload)
        print(f"Published: {payload}")        
        
        time.sleep(config["loop_interval"])

if __name__ == "__main__":
    main()

