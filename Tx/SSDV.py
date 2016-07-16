from Transmit import tx
from time import sleep
file = open("/home/pi/test.bin", "rb")
data = file.read(256)
tx(list(bytearray(data)))
