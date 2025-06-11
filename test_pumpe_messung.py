import snap7
import struct
import time
from snap7.type import Areas

PLC_IP = "172.19.10.53"
RACK = 0
SLOT = 2

# Verbindung herstellen
plc = snap7.client.Client()
plc.connect(PLC_IP, RACK, SLOT)

if not plc.get_connected():
    print("❌ Verbindung fehlgeschlagen.")
    exit()

# Benutzerwert eingeben
try:
    drehzahl = int(input("🔧 Drehzahlwert (0–28000): "))
    drehzahl = max(0, min(drehzahl, 28000))  # Begrenzung
except ValueError:
    print("⚠️ Ungültiger Wert. Abbruch.")
    plc.disconnect()
    exit()

# Pumpe aktivieren
plc.write_area(Areas.PA, 0, 3, struct.pack('>h', drehzahl))
print(f"🚰 Pumpe läuft mit {drehzahl} für 10 Sekunden...\n")

# Werte aufzeichnen
for sek in range(100):
    # Füllstand B102 (%IW3) auslesen
    daten = plc.read_area(Areas.PE, 0, 3, 2)
    rohwert = int.from_bytes(daten, byteorder='big', signed=True)

    # Umrechnung auf mm (Beispiel: 32767 entspricht 300 mm)
    fuellstand_mm = rohwert * 0.02286 - 277.86


    print(f"⏱️ Sekunde {sek+1}: Rohwert = {rohwert}, Füllstand ≈ {fuellstand_mm:.1f} mm")
    time.sleep(1)

# Pumpe deaktivieren
plc.write_area(Areas.PA, 0, 3, struct.pack('>h', 0))
print("\n🛑 Pumpe gestoppt.")

plc.disconnect()
print("🔌 Verbindung zur SPS getrennt.")
