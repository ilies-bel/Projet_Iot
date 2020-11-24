#!/bin/sh


service influxdb start
influx

sleep 5

python3 controller.py
