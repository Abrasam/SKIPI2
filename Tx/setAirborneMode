import serial,sys,struct
from timeout import *
def send(s):
    with serial.Serial("/dev/ttyAMA0", 75, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_TWO) as r:
        r.flush()
        for c in s:
            r.write(c)
            r.flush()
        r.flush()
try:
    with timeout(seconds=30):
        x = [0xB5, 0x62, 0x06, 0x24, 0x24, 0x00, 0xFF, 0xFF, 0x06,
         0x03, 0x00, 0x00, 0x00, 0x00, 0x10, 0x27, 0x00, 0x00,
         0x05, 0x00, 0xFA, 0x00, 0xFA, 0x00, 0x64, 0x00, 0x2C,
         0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
         0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x16, 0xDC]
        z = []
        success = False
        while not success:
            for y in x:
                z.append(chr(y))
            g = serial.Serial("/dev/ttyAMA0", 9600, timeout=1)
            g.write(chr(0xFF))
            for y in x:
                g.write(chr(y))
            g.flush()
            for i in range(0, 20):
                st = ""
                s = g.readline()
                for v in s:
                    st += hex(int(v.encode('hex'), 16)) + " "
                if "0xb5 0x62 0x5 0x1 0x2 0x0 0x6 0x24 0x32 0x5b" in st:
                    print("GPS Success")
                    send("Success.")
                    success = True
                    break
            g.close()
except:
    print("ERRORS!")
    send("GPS Fail.")
