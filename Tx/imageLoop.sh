#!/bin/bash
while true; do
    ID="`head -n 1 count.txt`"
    String="`date +%s`.jpg"
    echo "Saving to $String"
    raspistill -o "/home/pi/images/$String"
    convert -resize 768x576 "/home/pi/images/$String" /home/pi/tmp.jpg
    ./ssdv -e -c REGGIE -i "$ID" /home/pi/tmp.jpg /home/pi/tmp.bin
    python increment.py
    sleep 60s
done
