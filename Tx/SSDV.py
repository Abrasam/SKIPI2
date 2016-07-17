from Transmit import txMulti
from time import sleep
def sendImage():
    file = open("/home/pi/tmp.bin", "rb")
    data = file.read(256)
    add = data
    while add != "":
        add = file.read(256)
        data += add
    txMulti(list(bytearray(data)))

sendImage()
