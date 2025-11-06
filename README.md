Note: Project in progress

# Intro
This project provides the simple environmental-control system based on low-cost sensors, designed for monitornig greenhouse environment. 

Raspberry Pi is the main device that captures measurement data from ESP32 Wi-Fi module using MQTT protocol.
 
## Quick start:
- All the code from /esp_setup needs to be copied to ESP32, then it will start to perform measurements and expose it in MQTT thread
- listen.py has to be running on RPi- that will capture results and save it to file in /data folder.
- Use gen_plot.py to create plot with chosen type of measurements from specified data file

Currently supported sensors:
- bme280 - returns temperature, pressure and humidity
- dht11 - returns temperature and humidity
- ds18b20 - returns temperature, works in liquids

Moisture sensors in testing.

# Raspberry Pi initial setup
## To use ssh- configure Ethernet connection 
#### Set IP on Mac (or find the equivalent for your system):
    System Settings > Network > Ethernet
    DHCP> Manually
    IP: 192.168.2.1
    Subnet Mask: 255.255.255.0

#### On RPi- create and activate new static Ethernet connection
    sudo nmcli con add type ethernet ifname eth0 con-name static-eth0 ipv4.addresses 192.168.2.2/24 ipv4.method manual
    sudo nmcli c up static-eth0

    The IP is now set to 192.168.2.2
 
## Configure RPi as a Wi-Fi access point:
#### Add new wifi-connection:
    nmcli connection add type wifi ifname wlan0 con-name esp32-ap autoconnect yes ssid ESP32_AP

#### Secure it to Access Point mode with shared networking:
    nmcli connection modify esp32-ap 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared

#### Secure the network with WPA2:
    nmcli connection modify esp32-ap wifi-sec.key-mgmt wpa-psk wifi-sec.psk "supersecretpassword"
 
#### Specify encryption parameters for enahnced security:
    nmcli connection modify esp32-ap \
    802-11-wireless-security.key-mgmt wpa-psk \
    802-11-wireless-security.proto rsn \
    802-11-wireless-security.pairwise ccmp

#### Restart the connection:
    nmcli connection down esp32-ap
    nmcli connection up esp32-ap

#### Check AP's IP address:
    ip a show wlan0

#### If you want to set stable IP for the AP:
    sudo nmcli connection modify RPi_AP ipv4.method shared ipv4.addresses 192.168.4.1/24

# ESP32 setup

#### Install dependencies:
    python3 -m pip install --upgrade pip esptool mpremote

#### Find the serial port (probably it's /dev/ttyUSB0):
    ls /dev/ttyUSB*

#### Download ESP MicroPython firmware

#### Erase flash:
    esptool --chip esp32 --port <PORT> --baud 460800 erase_flash

#### Flash MicroPython:
    esptool --chip esp32 --port <PORT> --baud 460800 write_flash -z 0x10    00 ~/Downloads/ESP32_GENERIC-*.bin

#### Verify if you can enter REPL:
    mpremote connect <PORT> repl

#### Copy files from esp_setup to ESP32:
    cd esp_setup
    mpremote connect <PORT> fs cp -r  * :

#### Confirm that files were copied:
    mpremote connect <PORT> fs ls -l

#### Reboot the ESP32 and watch the logs
    mpremote connect <PORT> reset
    mpremote connect <PORT> repl (Ctrl-X to close)
