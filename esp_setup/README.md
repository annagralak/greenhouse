# ESP32 setup
This module handles sensor data acquisition and publishes readings via MQTT.

Each ESP32 acts as an independent data source.
Multiple ESP32 devices are supported and can publish to different topics.

## ESP32 initial setup

#### Install dependencies:
```
    python3 -m pip install --upgrade pip esptool mpremote
```

#### Find the serial port (probably it's /dev/ttyUSB0):
```
    ls /dev/ttyUSB*
```

#### Download ESP MicroPython firmware
Download latest firmware for ESP32 (e.g. ESP32_GENERIC-*.bin)

#### Erase flash:
```
    esptool --chip esp32 --port <PORT> --baud 460800 erase_flash
```

#### Flash MicroPython:
```
    esptool --chip esp32 --port <PORT> --baud 460800 write_flash -z 0x1000 ~/Downloads/ESP32_GENERIC-*.bin
```

#### Verify if you can enter REPL:
```
    mpremote connect <PORT> repl
```

#### Upload project files to ESP32:
```
    cd esp_setup
    mpremote connect <PORT> fs cp -r  * :
```

#### Confirm that files were copied:
```
    mpremote connect <PORT> fs ls -l
```

#### Reboot the ESP32 and watch the logs
```
    mpremote connect <PORT> reset
    mpremote connect <PORT> repl (Ctrl-X to close)
```
Exit REPL with Ctrl-X

## Configuration
### Config file
The ESP32 uses a JSON config file.

#### Example:
```
{
  "id": "esp32-1",
  "topic": "greenhouse/esp32-1",
  "mqtt_broker": "192.168.4.1",
  "mqtt_port": 1883,
  "loop_interval": 60,

  "sensors": [
    {
      "id": "bme280_1",
      "type": "bme280",
      "config": {
        "i2c_scl": 22,
        "i2c_sda": 21
      }
    },
    {
      "id": "ds18b20_1",
      "type": "ds18b20",
      "config": {
        "pin": 15
      }
    }
  ]
}
```

#### Config fields:
Device:
- id — unique identifier for this ESP32
- topic — MQTT topic used for publishing (should be unique per device)

MQTT:
- mqtt_broker — IP address of broker
- mqtt_port — usually 1883

Loop:
- loop_interval — seconds between measurements

Sensors:

Each sensor defines:
- id — unique sensor name (used in output JSON)
- type — sensor driver type
- config — hardware-specific settings

### Wi-Fi configuration
The ESP32 connects to your network using credentials stored in a local file.

Create a file named wifi_credentials.json. Place it in the root directory of the ESP32 filesystem (same level as main.py after upload).

It should look like this:
```
{
  "ssid": "your_network_name",
  "password": "your_password"
}
```

## Output format
Example payload:
```
{
  "bme280_1": {
    "temperature": 22.3,
    "humidity": 52.4,
    "pressure": 101567
  },
  "ds18b20_1": {
    "temperature": 21.3125
  }
}
```

## Multiple ESP32 devices
You can run multiple ESP32 units in parallel.

Each device must have a unique:
- id
- topic

All devices can publish to the same MQTT broker.

## Notes:
- I2C sensors require proper wiring (SDA/SCL)
- DS18B20 requires pull-up resistor
- ESP32 must be able to connect to the MQTT broker (correct IP, same network, port 1883 open)