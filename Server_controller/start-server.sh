#!/bin/sh


service influxdb start

sleep 2
sudo python3 controller.py
