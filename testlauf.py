from main import zyklus
from fuellstand_log import reset_logdatei, plot_fuellstaende
from steuerung import stoppe_pumpe, init_plc, beenden
from sensoren import sensorwerte, auslesen_sensoren
import threading
import time

stop_event = threading.Event()
sollwert_mm = 100

def schneller_sensor_loop():
    while not stop_event.is_set():
        auslesen_sensoren()
        time.sleep(0.5)

def testlauf():
    global sollwert_mm
    print("🚀 Starte Testlauf")

    eingabe = input("🔧 Ventil offen? (j/n): ").strip().lower()
    sensorwerte["v104_offen"] = eingabe == "j"
    print(f"🔁 Ventilstatus gesetzt: {'offen' if sensorwerte['v104_offen'] else 'geschlossen'}")

    soll_input = input("🎯 Soll-Füllstand in mm (z. B. 100): ").strip()
    sollwert_mm = max(20, min(178, int(soll_input)))
    print(f"🎯 Sollwert gesetzt auf {sollwert_mm} mm")

    reset_logdatei()
    sensor_thread = threading.Thread(target=schneller_sensor_loop, daemon=True)
    sensor_thread.start()

    start = time.time()
    while time.time() - start < 15:
        zyklus()
        time.sleep(1)

    print("✅ Testlauf abgeschlossen – Pumpe wird gestoppt...")

    try:
        plc = init_plc()
        stoppe_pumpe(plc)
        beenden(plc)
    except Exception as e:
        print(f"⚠️ Fehler beim Stoppen der Pumpe: {e}")

    stop_event.set()
    sensor_thread.join()
    plot_fuellstaende()

if __name__ == "__main__":
    testlauf()



"""    
    fuellstand_sim = (median_sim - 11000) * skala +20

    letzter_fuellstand_sim = fuellstand_sim"""