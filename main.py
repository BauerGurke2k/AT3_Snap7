import time
import threading
from steuerung import plc, beenden, TESTMODUS
from sensoren import auslesen_sensoren
from regelung import ansteuerung
from simulation import simuliere_behaelter
from environment import sensorwerte
from fuellstand_log import log_fuellstaende, plot_fuellstaende, reset_log

stop_event = threading.Event()

def schneller_sensor_loop():
    while not stop_event.is_set():
        auslesen_sensoren()
        time.sleep(0.5)

def zyklus(sollwert_mm):
    if TESTMODUS:
        auslesen_sensoren()
        ansteuerung(sollwert_mm)
        simuliere_behaelter()
    else:
        auslesen_sensoren()
        ansteuerung(sollwert_mm)
        simuliere_behaelter()

    log_fuellstaende()

if __name__ == "__main__":
    print("▶️ Starte Steuerungssystem... (Strg+C zum Beenden)")

    ventil_input = input("🔧 Ventil offen? (j/n): ").strip().lower()
    sensorwerte["v104_offen"] = ventil_input == "j"
    print(f"🔁 Ventilstatus gesetzt: {'offen' if sensorwerte['v104_offen'] else 'geschlossen'}")

    sollwert_mm = int(input("🎯 Soll-Füllstand in mm (z. B. 100): ").strip())
    print(f"🎯 Sollwert gesetzt auf {sollwert_mm} mm")

    plc.connect()
    print("✅ SPS-Verbindung hergestellt")

    reset_log()
    sensor_thread = threading.Thread(target=schneller_sensor_loop, daemon=True)
    sensor_thread.start()

    try:
        while True:
            zyklus(sollwert_mm)
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n🛑 Steuerung beendet durch Benutzer")
        stop_event.set()
        sensor_thread.join()
        plot_fuellstaende()
        beenden(plc)

#b101 max = 300mm
#b101 min = 136mm
#startwert b101 = max
#b102 max = 178mm
#b102 min = 20mm
#startwert b102 = min