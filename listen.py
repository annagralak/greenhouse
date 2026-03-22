import argparse
import json
import os
import time
import paho.mqtt.client as mqtt
from datetime import datetime

CONFIG_FILE = "mqtt_config.json"

def load_config(path=CONFIG_FILE):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load config {path}: {e}")
        return None

def update_timestamp(data):
    """Replace all 'timestamp' values exposed by ESP32 by the current time from RPi system."""
    now_str = time.strftime("%Y-%m-%d %H:%M", time.localtime())
    for sensor in data.values():
        if 'timestamp' in sensor:
            sensor['timestamp'] = now_str
    return data

def pretty_print(data, indent=0):
    """Recursively print JSON"""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{key}:")
                pretty_print(value, indent + 1)
            else:
                print(f"\t{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"- [{i}]")
            pretty_print(item, indent + 1)
    else:
        print(f"{data}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {userdata['broker']}:{userdata['port']}")

        for topic in userdata["topics"]:
            client.subscribe(topic)
            print(f"Subscribed to topic: {topic}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        # This line should be commented out if timestamp from ESP32 should be used      
        data = update_timestamp(data)

        print(f"\n--- Sensor Update from {msg.topic} ---")
        pretty_print(data)

        # Prepare JSON entry
        entry = {
            "topic": msg.topic,
            "data": data,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }

        fname = userdata["filename"]
        os.makedirs(os.path.dirname(fname), exist_ok=True)

        # Append one JSON object per line
        with open(fname, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, separators=(',', ':'), ensure_ascii=False) + "\n")

    except Exception as e:
        print(f"Error parsing message: {e}")
        print("Raw payload:", msg.payload)

def create_new_file():
    os.makedirs("data", exist_ok=True)
    filename = os.path.join("data", datetime.now().strftime("data_%Y%m%d_%H%M%S.json"))

    return filename 
    
if __name__ == "__main__":

    config = load_config()
    if not config:
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Optional filename for output")
    args = parser.parse_args() 

    filename = args.output if args.output else create_new_file()

    userdata = {
        "filename": filename,
        "broker": config["mqtt_broker"],
        "port": config.get("mqtt_port", 1883),
        "topics": config.get("topic_list", [])
    }

    client = mqtt.Client(userdata=userdata)
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("Starting MQTT subscriber...")
    client.connect(userdata["broker"], userdata["port"], 60)
    client.loop_forever()
    
    

