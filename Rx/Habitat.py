import requests, hashlib, base64, sys, threading, os
from time import strftime
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from time import sleep

toSend = {"telemetry" : "", "ssdv" : []}

class LoRaReceive(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceive, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        val = self.read_payload(nocheck=True)
        rows,columns = os.popen("stty size", "r").read().split()
        if (str(bytearray(val))[:2] == "$$"):
            sys.stdout.write("\r" + str(bytearray(val))[:-1])
            toSend["telemetry"] = str(bytearray(val))
            sys.stdout.write((int(columns)-len(val)-19)*" " + "(Received: " + strftime("%H:%M:%S)"))
        else:
            sys.stdout.write("\rImage packet.")
            addToImagePacket(str(bytearray(val)))
            sys.stdout.write((int(columns)-33)*" " + "(Received: " + strftime("%H:%M:%S)"))
        sys.stdout.flush()
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(1)

def uploadTelemetry():
    global toSend
    while True:
        try:
            telemetry = toSend["telemetry"]
            if not telemetry == "":
                b64 = (base64.b64encode(telemetry.encode()))
                sha256 = hashlib.sha256(b64).hexdigest()
                b64 = b64.decode()
                now = strftime("%Y-%0m-%0dT%H:%M:%SZ")
                json = "{\"data\": {\"_raw\": \"%s\"},\"receivers\": {\"%s\": {\"time_created\": \"%s\",\"time_uploaded\": \"%s\"}}}" % (b64, "SAMPI", now, now)
                #print(json)
                #print(sha256)
                headers = {"Accept" : "application/json", "Content-Type" : "application/json", "charsets" : "utf-8"}
                try:
                    r = requests.put("http://habitat.habhub.org/habitat/_design/payload_telemetry/_update/add_listener/"+sha256, headers=headers, data=json, timeout=2)
                except:
                    sys.stdout.write("\rError while uploading. Internet OK?")
                #print(r.status_code)
                #print(r.content)
                if telemetry == toSend["telemetry"]:
                    toSend["telemetry"] = ""
        finally:
            sleep(5)

def addToImagePacket(part):
    if len(part) == 255:
        part = "U" + part
        toSend["ssdv"].append(part)

def uploadSSDVPackets():
    global toSend
    while True:
        try:
            sent = []
            for packet in toSend["ssdv"]:
                b64 = base64.b64encode(bytes(packet)).decode('utf-8')
                headers = {"Accept" : "application/json", "Content-Type" : "application/json", "charsets" : "utf-8"}
                now = strftime("%Y-%0m-%0dT%H:%M:%SZ")
                upload = "{\"type\": \"packet\", \"packet\": \"%s\", \"encoding\": \"base64\", \"received\": \"%s\", \"receiver\": \"%s\"}" % (b64, now, "SAMPI")
                try:
                    r = requests.post("http://ssdv.habhub.org/api/v0/packets", headers=headers, data=upload, timeout=2)
                except:
                    sys.stdout.write("\rError while uploading. Internet OK?")
                #print(r.content)
                #print(r.status_code)
                sent.append(packet)
                sleep(0.5)
            for packet in sent:
                toSend["ssdv"].remove(packet)
        finally:
            sleep(0.1)

BOARD.setup()

lora = LoRaReceive(verbose=False)
lora.set_mode(MODE.STDBY)
lora.set_freq(868.000000)
lora.set_pa_config(pa_select=1)
lora.set_bw(8)

TeleThread = threading.Thread(target=uploadTelemetry)
SSDVThread = threading.Thread(target=uploadSSDVPackets)
TeleThread.daemon = True
SSDVThread.daemon = True
TeleThread.start()
SSDVThread.start()

print("Latest transmission:")

try:
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()

