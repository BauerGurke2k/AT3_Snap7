from steuerung import steuere_pumpe, plc
from environment import sensorwerte

def ansteuerung(sollwert_mm):
    fuellstand = sensorwerte["fuellstand_b101"]
    hysterese = 20

    if fuellstand < (sollwert_mm - hysterese):
        steuere_pumpe(plc, 24000)
    elif fuellstand > (sollwert_mm + hysterese):
        steuere_pumpe(plc, 0)
