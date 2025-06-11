from steuerung import steuere_pumpe, plc
from environment import b102
from environment import TESTMODUS,steuerdaten


motordrehzahl = 24000


def ansteuerung(sollwert_mm):
    fuellstand = b102.fuellstand
    global motordrehzahl
    hysterese = 20
    if TESTMODUS:
        if fuellstand < (sollwert_mm - hysterese):
            steuerdaten["letzter_pumpenwert"] = motordrehzahl 
        elif fuellstand > (sollwert_mm + hysterese):
            steuerdaten["letzter_pumpenwert"] = 0
        else:
            pass
    else:
        if fuellstand < (sollwert_mm - hysterese):
            steuere_pumpe(plc, motordrehzahl)
        elif fuellstand > (sollwert_mm + hysterese):
            steuere_pumpe(plc, 0)
        else:
            pass
    print(f"wird angesteuert{fuellstand}")
    return steuerdaten["letzter_pumpenwert"] 
