from steuerung import steuere_pumpe, plc
from environment import b102
from environment import TESTMODUS,steuerdaten
#from simulation import fuellstand_real,fuellstand_sim
import simulation

motordrehzahl = 24000
max_pumpendrehzahl = 28000

def ansteuerung(sollwert_mm):
    
    global motordrehzahl
    hysterese = 20
    if TESTMODUS == False :

        if simulation.fuellstand_real < (sollwert_mm - hysterese):
            steuere_pumpe(plc, motordrehzahl)

        elif simulation.fuellstand_real > (sollwert_mm + hysterese):
            steuere_pumpe(plc, 0)
       

        else:
            pass

        if b102.fuellstand < (sollwert_mm - hysterese):
            steuerdaten["letzter_pumpenwert"] = motordrehzahl 
            print(f"fuellstand in regl{simulation.fuellstand_sim},{steuerdaten["letzter_pumpenwert"]}")
        elif b102.fuellstand > (sollwert_mm + hysterese):
            steuerdaten["letzter_pumpenwert"] = 0
            print(f"fuellstand in regl{simulation.fuellstand_sim},{steuerdaten["letzter_pumpenwert"]}")
        else:
            pass
    else:
        if b102.fuellstand < (sollwert_mm - hysterese):
            steuerdaten["letzter_pumpenwert"] = motordrehzahl 
            print(f"fuellstand in regl{simulation.fuellstand_sim},{steuerdaten["letzter_pumpenwert"]}")
        elif b102.fuellstand > (sollwert_mm + hysterese):
            steuerdaten["letzter_pumpenwert"] = 0
            print(f"fuellstand in regl{simulation.fuellstand_sim},{steuerdaten["letzter_pumpenwert"]}")
        else:
            pass
        
    
    #print(f"wird angesteuert{fuellstand}")
    return steuerdaten["letzter_pumpenwert"] 
