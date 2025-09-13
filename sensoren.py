import snap7
from snap7.type import Areas
from collections import deque
import statistics
from simulation import k,pumpenkonstante,abflusskonstante
from regelung import motordrehzahl,max_pumpendrehzahl
from environment import TESTMODUS,steuerdaten
import random


PLC_IP = "172.19.10.53"
RACK = 0
SLOT = 2

# Puffer für Median-Glättung
rohwert_puffer = deque(maxlen=9)
rohwert_puffer_sim = deque(maxlen=9)
median_mess = 11000
median_sim = 11000
roh_b102_simuliert = 11000 
zykluszeit_mess = 0.2


def auslesen_sensoren():
    global roh_b102_simuliert
    try:
        global median_mess
        global median_sim
        randomfaktor = random.uniform(0.98,1.03)
        delta_sensorwert_sim =  (pumpenkonstante*(motordrehzahl/max_pumpendrehzahl)*zykluszeit_mess)
        delta_abfluss_sim = abflusskonstante * zykluszeit_mess 

        if TESTMODUS == False:
            


            plc = snap7.client.Client()
            plc.connect(PLC_IP, RACK, SLOT)
            roh_b102 = int.from_bytes(plc.read_area(Areas.PE, 0, 3, 2), 'big', signed=True)
            plc.disconnect()
            #print (f"roh: {roh_b102}")

            rohwert_puffer.append(roh_b102)
        

            if len(rohwert_puffer) >= 5:

                median_mess = statistics.median(rohwert_puffer)
                print(f"medimess{median_mess}")
            
            

            if steuerdaten['letzter_pumpenwert'] > 7000:
                

                roh_b102_simuliert = round((roh_b102_simuliert + delta_sensorwert_sim) * randomfaktor, 1)
               
                if roh_b102_simuliert > 18500:
                    roh_b102_simuliert = 18500
                #print (f"roh: {roh_b102_simuliert}")
            else:
                roh_b102_simuliert = round(((roh_b102_simuliert - delta_abfluss_sim)* randomfaktor ),1)
                
                if roh_b102_simuliert < 11000:
                    roh_b102_simuliert = 11000
                
            
            rohwert_puffer_sim.append(roh_b102_simuliert)
            
            if len(rohwert_puffer_sim) >= 5:
                median_sim = statistics.median(rohwert_puffer_sim)

                if median_sim > 18500:
                    median_sim = 18500

                print(f"medisim {median_sim}")

        else:

            randomfaktor = random.uniform(0.999,1.001)
            delta_sensorwert_sim =  (pumpenkonstante*(motordrehzahl/max_pumpendrehzahl)*zykluszeit_mess)
            delta_abfluss_sim = abflusskonstante * zykluszeit_mess 
            if steuerdaten['letzter_pumpenwert'] > 7000:
                

                roh_b102_simuliert = round((roh_b102_simuliert + delta_sensorwert_sim) * randomfaktor, 1)
               
                if roh_b102_simuliert > 18500:
                    roh_b102_simuliert = 18500
                #print (f"roh: {roh_b102_simuliert}")
            else:
                roh_b102_simuliert = round(((roh_b102_simuliert - delta_abfluss_sim)* randomfaktor ),1)
                
                if roh_b102_simuliert < 11000:
                    roh_b102_simuliert = 11000
                
            
            rohwert_puffer_sim.append(roh_b102_simuliert)
            
            if len(rohwert_puffer_sim) >= 5:
                median_sim = statistics.median(rohwert_puffer_sim)

                if median_sim > 18500:
                    median_sim = 18500

                print(f"medisim {median_sim}")



            
                
             


    except Exception as e:
        print(f"⚠️ Fehler in auslesen_sensoren(): {e}")
