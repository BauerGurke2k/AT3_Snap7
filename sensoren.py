import snap7
from snap7.type import Areas
from collections import deque
import statistics

# Schalter für Testbetrieb ohne SPS
TESTMODUS = False

PLC_IP = "172.19.10.53"
RACK = 0
SLOT = 2

sensorwerte = {
    "fuellstand_b101": 0,
    "fuellstand_b102": 0,
    "rohwert_b102": 0,
    "pumpenwert": 0,
    "v104_offen": False
}

# Puffer für Median-Glättung
rohwert_puffer = deque(maxlen=9)

def auslesen_sensoren():
    try:
        if TESTMODUS:
            roh_b102 = 14200  # fixer Wert im Test
        else:
            plc = snap7.client.Client()
            plc.connect(PLC_IP, RACK, SLOT)
            roh_b102 = int.from_bytes(plc.read_area(Areas.PE, 0, 3, 2), 'big', signed=True)
            plc.disconnect()

        sensorwerte["rohwert_b102"] = roh_b102
        rohwert_puffer.append(roh_b102)

        # Median statt gleitendem Mittelwert
        if len(rohwert_puffer) >= 3:
            rohwert_median = statistics.median(rohwert_puffer)

            # Neue Umrechnung: 11000 → 20 mm, 18500 → 178 mm
            skala = 158 / (18500 - 11000)
            fuellstand_mm = (rohwert_median - 11000) * skala + 20
            sensorwerte["fuellstand_b102"] = round(fuellstand_mm, 1)

        print(f"📊 Sensorwerte: {{'fuellstand_b101': {sensorwerte['fuellstand_b101']} mm, 'fuellstand_b102': {sensorwerte['fuellstand_b102']} mm}}")

    except Exception as e:
        print(f"⚠️ Fehler in auslesen_sensoren(): {e}")
