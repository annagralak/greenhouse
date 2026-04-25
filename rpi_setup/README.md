# Raspberry Pi setup
The Raspberry Pi acts as the central system controller for the greenhouse project.

It is responsible for:
- Receiving sensor data via MQTT
- Maintaining system state
- Evaluating rules
- Controlling relays (heating, lighting)
- Logging data
- Generating plots from stored data

## System overview
```
ESP32 Devices
     ↓ (MQTT)
MQTT Broker (Raspberry Pi)
     ↓
Python Backend
 ├── State Store
 ├── Rule Engine
 ├── Relay Controller
 ├── Logger (JSON files)
 └── Plot Generator
 ```

- ESP32 sends sensor data via MQTT
- Raspberry Pi receives and stores it
- Rules are evaluated in real time
- Relays are switched automatically
- Data is logged continuously
- Plots are generated from stored logs in a standalone script

## Quick start

```
ssh pi@192.168.2.2
source venv/bin/activate
python3 main.py
```

## Configuration file
The system uses a JSON config file to define MQTT connection, relays, and rules.

Example:
```
{
  "mqtt_broker": "localhost",
  "mqtt_port": 1883,
  "topic_list": ["greenhouse/esp32-1"],

  "relays": [
    {
      "id": "heating_relay",
      "type": "gpio",
      "config": { "pin": 17 }
    }
  ],

  "rules": [
    {
      "type": "temperature_control",
      "sensor": "dht11_1",
      "field": "temperature",
      "relay": "heating_relay",
      "on_below": 19,
      "off_above": 21
    }
  ]
}
```

#### MQTT settings
- mqtt_broker — broker IP / hostname
- mqtt_port — usually 1883
- topic_list — subscribed ESP32 topics

#### Relays
Defines physical outputs controlled by Raspberry Pi:
- id — relay name used in rules
- type — hardware type (e.g. GPIO)
- config.pin — GPIO pin number

#### Rules
Rule types supported:
- temperature_control — controls relay based on sensor thresholds
- time_control — switches relay based on time of day

Each rule typically defines:
- sensor + field
- condition thresholds or time window
- target relay

## Plot generation
The gen_plot.py script generates time-series plots from stored sensor data files.

#### Usage
```
python3 gen_plot.py <filename> [options]
```

Arguments:
- filename — path to data file, required
- -t / --temperature — plots temperature
- -hu / --humidity — plots humidity
- -p / --pressure — plots pressure
- -m / --moisture — plots moisture
- --topic — filters by MQTT topic
- -o / --output — output filename prefix, uses input filename by default

Example usage:
```
python3 gen_plot.py data/data_2026-01-01.jsonl \
  -t -hu -p -m \
  --topic greenhouse/esp32-1 \
  -o greenhouse_plot
```

#### Note
If you run the script over SSH and want to display plots, you must enable X11 forwarding:
```
ssh -X pi@192.168.2.2
```

## Raspberry Pi network setup
### Configure Ethernet connection 
#### Set static IP on Mac (or find the equivalent for your system)
```
    System Settings > Network > Ethernet
    DHCP> Manually
    IP: 192.168.2.1
    Subnet Mask: 255.255.255.0
```

#### On RPi- create and activate new static Ethernet connection
```
    sudo nmcli con add type ethernet ifname eth0 con-name static-eth0 ipv4.addresses 192.168.2.2/24 ipv4.method manual
    sudo nmcli c up static-eth0
```
The IP is now set to 192.168.2.2
 
### Configure RPi as a Wi-Fi access point
The Raspberry Pi can act as a Wi-Fi access point for ESP32 devices.

#### Create AP network
```
    nmcli connection add type wifi ifname wlan0 con-name esp32-ap autoconnect yes ssid ESP32_AP
```

#### Enable AP mode
```
    nmcli connection modify esp32-ap 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
```

#### Set password (WPA2)
```
    nmcli connection modify esp32-ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk "supersecretpassword"
```
 
#### Apply stronger encryption settings
```
    nmcli connection modify esp32-ap \
    802-11-wireless-security.key-mgmt wpa-psk \
    802-11-wireless-security.proto rsn \
    802-11-wireless-security.pairwise ccmp
```

#### Restart AP
```
    nmcli connection down esp32-ap
    nmcli connection up esp32-ap
```

#### Check AP's IP address:
```
    ip a show wlan0
```

#### Optional: fixed AP IP
```
    sudo nmcli connection modify RPi_AP ipv4.method shared ipv4.addresses 192.168.4.1/24
```

## Notes
- MQTT broker must be running before ESP32 connects
- ESP32 and Pi must be on same network (or AP mode)
- Ensure /data directory exists for logs
- Always use SSH with -X for plotting



