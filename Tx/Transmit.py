from time import sleep
from timeout import *
from SX127x.LoRa import *
from SX127x.board_config import BOARD

class LoRaTransmit(LoRa):

    transmitting = False

    def __init__(self, verbose=False):
        super(LoRaTransmit, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([1,0,0,0,0,0])
        
    def on_tx_done(self):
        self.set_mode(MODE.SLEEP)
        self.transmitting = False
        self.set_mode(MODE.STDBY)

    def send(self, message):
        if not self.transmitting:
            self.set_mode(MODE.STDBY)
            self.set_payload_length(len(message))
            self.write_payload(message)
            self.transmitting = True
            self.set_mode(MODE.TX)
    def start(self, msg):
        self.send(msg)
        while self.transmitting:
            sleep(5)

def tx(msg):
    BOARD.setup()
    lora = LoRaTransmit()
    lora.set_freq(868.000000)
    lora.set_pa_config(pa_select=1, max_power=5)
    lora.set_bw(8)
    lora.set_coding_rate(CODING_RATE.CR4_5)
    try:
        lora.send(msg)
    finally:
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()

def txMulti(msg):
    BOARD.setup()
    lora = LoRaTransmit()
    lora.set_freq(868.000000)
    lora.set_pa_config(pa_select=1, max_power=5)
    lora.set_bw(8)
    lora.set_coding_rate(CODING_RATE.CR4_5)
    try:
        while len(msg) > 0:
            part = msg[:128]
            msg = msg[128:]
            lora.send(part)
            try:
                with timeout(seconds=2):
                    while lora.transmitting:
                        sleep(0.1)
            except TimeoutError:
                print("Sending timed out.")
    finally:
        lora.set_mode(MODE.SLEEP)
        BOARD.teardown()
