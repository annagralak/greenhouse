#!/usr/bin/env bash

mosquitto_sub -h localhost -t "greenhouse/esp32-1/sensors"

