#!/bin/bash
screen -mSd gps
screen -S gps -X stuff "python GPSLoop.py\n"
while true; do
    python Telemetry.py
    sleep 0.5
done
