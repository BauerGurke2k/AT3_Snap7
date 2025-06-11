import snap7
from snap7.util import set_int
from snap7.type import Areas
import environment

TESTMODUS = False

class SPS:
    def __init__(self, ip='172.19.10.53', rack=0, slot=2):
        self.client = snap7.client.Client()
        self.ip = ip
        self.rack = rack
        self.slot = slot

    def connect(self):
        self.client.connect(self.ip, self.rack, self.slot)

    def write_drehzahl(self, drehzahl):
        data = bytearray(2)
        set_int(data, 0, drehzahl)
        self.client.write_area(Areas.DB, 1, 0, data)

    def disconnect(self):
        self.client.disconnect()

plc = SPS()

def steuere_pumpe(plc_obj, drehzahl):
    environment.steuerdaten["letzter_pumpenwert"] = drehzahl
    plc_obj.write_drehzahl(drehzahl)

def beenden(plc_obj):
    steuere_pumpe(plc_obj, 0)
    plc_obj.disconnect()
    print("🔌 Verbindung zur SPS getrennt.")
