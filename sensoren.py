import snap7
from snap7.type import Areas
from collections import deque
import statistics
from simulation import k
from regelung import motordrehzahl
from environment import TESTMODUS,steuerdaten
import random


PLC_IP = "172.19.10.53"
RACK = 0
SLOT = 2

# Puffer für Median-Glättung
rohwert_puffer = deque(maxlen=9)
rohwert_median = None
roh_b102 = 11200 

def auslesen_sensoren():
    global roh_b102
    try:
        if TESTMODUS:
            if steuerdaten['letzter_pumpenwert'] > 7000:
                randomfaktor = random.uniform(0.97,1.05)
                roh_b102 = round((roh_b102 + (k* motordrehzahl))*randomfaktor,1)
                if roh_b102 > 18500:
                    roh_b102 = 18500
                #print (f"roh: {roh_b102}")
            else:
                randomfaktor = random.uniform(0.97,1.05)
                roh_b102 = round((roh_b102 - 2 )*randomfaktor,1)
                if roh_b102 < 11200:
                    roh_b102 = 11200
        else:
            plc = snap7.client.Client()
            plc.connect(PLC_IP, RACK, SLOT)
            roh_b102 = int.from_bytes(plc.read_area(Areas.PE, 0, 3, 2), 'big', signed=True)
            plc.disconnect()
            print (f"roh: {roh_b102}")

        rohwert_puffer.append(roh_b102)

        # Median statt gleitendem Mittelwert
        if len(rohwert_puffer) >= 5:
            global rohwert_median
            rohwert_median = statistics.median(rohwert_puffer)
            #print(f"median{rohwert_median}")
            if rohwert_median > 18500:
                    rohwert_median = 18500
            
    except Exception as e:
        print(f"⚠️ Fehler in auslesen_sensoren(): {e}")
