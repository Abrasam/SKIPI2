from Transmit import tx
from time import sleep
import serial, threading, datetime, crcmod, subprocess

checksum = crcmod.predefined.mkCrcFun('crc-ccitt-false')

def makeTelemetry(gpsData):
    data = gpsData.split(",")
    if len(data) > 9 and "GGA" in data[0]:
        id = datetime.datetime.now() - datetime.datetime(1970, 1, 1)
        id = int(id.total_seconds())
        lat = ("-" if data[3] == "S" else "") +  data[2]
        long = ("-" if data[5] == "W" else "") + (data[4])
        alt = data[9]
        sats = data[7]
        time = data[1][0:2] + ":" + data[1][2:4] + ":" + data[1][4:6]
        telemetry = "$$REGGIE," + str(id) + "," + time + "," + lat + "," + long + "," + alt + "," + sats
        csum = (hex(checksum(telemetry[2:],0xFFFF))).upper()
       # print(csum)
        telemetry += "*" + csum[2:] + "\n"
        return telemetry
    return ""

with open("gps.txt", 'r') as file:
    data = file.readline()
    telemetry = makeTelemetry(data)
    if not telemetry == "":
        print(telemetry)
        tx(list(bytearray(telemetry)))
