import requests, hashlib, base64
from time import strftime
#from SX127x.LoRa import *
#from SX127x.board_config import BOARD
from time import sleep

'''class LoRaReceive(LoRa):
    def __init__(self, verbose=False):
        super(LoRaReceive, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        print("Received Packet:")
        val = self.read_payload(nocheck=True)
        print(str(bytearray(val)))
        if (str(bytearray(val))[:2] == "$$"):
            uploadTelemetry(str(bytearray(val)))
        else:
            addToImagePacket(str(bytearray(val)))
        self.set_mode(MODE.SLEEP)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
            sleep(1)'''

def uploadTelemetry(telemetry):
    b64 = (base64.b64encode(telemetry.encode()))
    sha256 = hashlib.sha256(b64).hexdigest()
    b64 = b64.decode()
    now = strftime("%Y-%0m-%0dT%H:%M:%SZ")
    json = "{\"data\": {\"_raw\": \"%s\"},\"receivers\": {\"%s\": {\"time_created\": \"%s\",\"time_uploaded\": \"%s\"}}}" % (b64, "SAMPI", now, now)
    #print(json)
    #print(sha256)
    headers = {"Accept" : "application/json", "Content-Type" : "application/json", "charsets" : "utf-8"}
    r = requests.put("http://habitat.habhub.org/habitat/_design/payload_telemetry/_update/add_listener/"+sha256, headers=headers, data=json)
    #print(r.status_code)
    #print(r.content)

def addToImagePacket(part):
    if part[0] == "U":
        currentPacket = part
    else:
        currentPacket += part
    if len(currentPacket) >= 256:
        uploadSSDV(currentPacket)
        currentPacket = ""

def uploadSSDVPacket(packet):
    b64 = base64.b64encode(bytes(packet)).decode('utf-8')
    headers = {"Accept" : "application/json", "Content-Type" : "application/json", "charsets" : "utf-8"}
    now = strftime("%Y-%0m-%0dT%H:%M:%SZ")
    upload = "{\"type\": \"packet\", \"packet\": \"%s\", \"encoding\": \"base64\", \"received\": \"%s\", \"receiver\": \"%s\"}" % (b64, now, "SAMPI")
    r = requests.post("http://ssdv.habhub.org/api/v0/packets", headers=headers, data=upload)
    print(r.content)
    print(r.status_code)

currentPacket = ""    
x = [85, 102, 3, 120, 63, 96, 43, 0, 0, 8, 6, 0, 0, 0, 0, 219, 145, 113, 80, 146, 69, 95, 186, 132, 169, 60, 85, 22, 28, 212, 140, 88, 139, 170, 202, 232, 161, 152, 14, 20, 156, 103, 241, 172, 121, 18, 226, 231, 86, 91, 130, 142, 145, 239, 27, 194, 202, 25, 65, 3, 210, 183, 173, 190, 88, 217, 200, 200, 221, 207, 210, 177, 111, 204, 167, 86, 150, 64, 27, 202, 140, 187, 6, 219, 198, 21, 15, 127, 173, 43, 93, 129, 83, 77, 212, 38, 176, 129, 38, 128, 168, 50, 62, 214, 12, 50, 8, 57, 53, 181, 107, 123, 45, 213, 245, 186, 75, 229, 21, 147, 120, 124, 158, 192, 113, 143, 122, 230, 199, 218, 5, 131, 206, 100, 27, 99, 143, 113, 7, 174, 238, 216, 199, 21, 165, 28, 118, 207, 117, 98, 158, 84, 147, 70, 98, 145, 254, 78, 185, 207, 83, 211, 138, 152, 166, 164, 91, 150, 154, 22, 60, 69, 163, 189, 236, 207, 113, 0, 24, 85, 203, 40, 239, 234, 115, 92, 190, 155, 108, 255, 218, 246, 187, 99, 103, 195, 131, 181, 6, 73, 197, 116, 186, 161, 107, 71, 99, 107, 12, 246, 249, 139, 56, 98, 114, 199, 252, 41, 186, 53, 174, 156, 170, 156, 228, 181, 0, 13, 218, 114, 84, 97, 6, 210, 79, 64, 220, 159, 15, 73, 240, 153, 226, 84, 181, 150, 110, 6, 61, 143, 21, 6, 237, 199, 79, 90]
stuff = "".join(chr(val) for val in x)
print(stuff)
uploadSSDVPacket(x)        

'''BOARD.setup()

lora = LoRaReceive(verbose=False)
lora.set_mode(MODE.STDBY)
lora.set_freq(868.000000)
lora.set_pa_config(pa_select=1)
lora.set_bw(8)

try:
    lora.start()
finally:
    lora.set_mode(MODE.SLEEP)
    BOARD.teardown()
'''
