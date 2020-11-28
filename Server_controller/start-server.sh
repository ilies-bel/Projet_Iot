#!/bin/sh


service influxdb start
#influx

sleep 2
python3 controller.py
