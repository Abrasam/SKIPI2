from Transmit import txMulti
from time import sleep
file = open("/home/pi/test.bin", "rb")
data = file.read(256)
add = data
while add != "":
    add = file.read(256)
    data += add
txMulti(list(bytearray(data)))
