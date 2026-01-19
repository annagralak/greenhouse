import argparse
import csv
import json
import os
import time
import paho.mqtt.client as mqtt

from datetime import datetime

BROKER = "localhost"
TOPIC = "greenhouse/esp32-1/sensors"

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
        print(f"Connected to MQTT broker at {BROKER}")
        client.subscribe(TOPIC)
        print(f"Subscribed to topic: {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        # This line should be commented out if timestamp from ESP32 should be used      
        data = update_timestamp(data)

        print("\n--- Sensor Update ---")
        pretty_print(data)

    except Exception as e:
        print(f"Error parsing message: {e}")
        print("Raw payload:", msg.payload)

    fname = userdata["filename"]
        
    with open(fname, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([msg.topic, json.dumps(data)])

def create_new_file():
    # Creating file for data, tbd better later
    filename = os.path.join("data", datetime.now().strftime("data_%Y%m%d_%H%M%S.csv"))

    # Create the CSV file and write header (optional)
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["topic", "data"])

    return filename 
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Optional filename for CSV output")
    args = parser.parse_args() 

    filename = args.output if args.output else create_new_file()

    client = mqtt.Client(userdata={"filename": filename})
    client.on_connect = on_connect
    client.on_message = on_message
    
    print("Starting MQTT subscriber...")
    client.connect(BROKER, 1883, 60)
    client.loop_forever()
    
    
