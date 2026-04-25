# Greenhouse automation system
This project is a modular system for greenhouse monitoring and control.

It is designed to be:
- Config-driven
- Easily extensible (new sensors, rules, actuators)
- Decoupled via MQTT

Currently supported sensors:
- bme280 - temperature, pressure and humidity
- dht11 - temperature and humidity
- ds18b20 - temperature, works in liquids
- Moisture sensors in progress
 
# Architecture Overview 
```
[ Sensors (ESP32) ] 
    ↓ 
    MQTT Broker 
    ↓ 
[ Raspberry Pi ] 
    ├── State Store 
    ├── Rule Engine 
    ├── Logger 
    └── Relay Controller
```

# Data flow
ESP32 
- Reads sensor data
- Publishes JSON payloads via MQTT

Raspberry Pi:
- Updates internal state
- Logs incoming data
- Evaluates rules
- Controls relays (heating, lighting)

# Project structure
```
greenhouse/ 
├── esp_setup/ # ESP32 firmware and sensor configuration 
└──rpi_setup/ # Raspberry Pi logic (MQTT, rules, logging, relays) 
```

# Configuration
ESP32 config defines:
- sensors
- pins
- MQTT topic

Raspberry Pi config defines:
- MQTT broker
- relays
- rules (temperature, time, etc.)

For detailed configuration instructions, refer to:
```
greenhouse/
├── esp_setup/
│   └── README.md   # ESP32 configuration (sensors, pins, MQTT topic)
└── rpi_setup/
    └── README.md   # Raspberry Pi configuration (MQTT, relays, rules)
```