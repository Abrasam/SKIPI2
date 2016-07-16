import serial, datetime
from time import sleep
from timeout import *
def telemetryLoop():
    data = ""
    while True:
        try:
            with timeout(seconds=90):
                with serial.Serial("/dev/ttyAMA0", 9600, timeout=1) as g:
                    data = g.readline()
                    print(data)
                    start = datetime.datetime.now().second
                    while not ("GGA" in data):
                        data = g.readline()
                        print(data)
                        if datetime.datetime.now().second - start > 30:
                            break
                if "GGA" in data:
                    with open("gps.txt", "w") as file:
                        file.write(data)
        except TimeoutError:
            pass #Probably put some helpful message here.
telemetryLoop()
