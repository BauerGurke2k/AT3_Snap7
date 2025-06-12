import time
import threading
import schedule
from steuerung import plc, beenden
from sensoren import auslesen_sensoren,TESTMODUS
from simulation import simuliere_behaelter
from fuellstand_log import log_fuellstaende, plot_fuellstaende, reset_log,start_live_plot
from regelung import ansteuerung
from environment import steuerdaten

def messzyklus(stop_event):
    while not stop_event.is_set():
        auslesen_sensoren()
        time.sleep(0.2)
        #print(f"sensoren lesen")

def pumpenzyklus(sollwert_mm):
    simuliere_behaelter()
    ansteuerung(sollwert_mm)
    log_fuellstaende()


if __name__ == "__main__":
    stop_event = threading.Event()

    if TESTMODUS:
        print("▶️ Starte Steuerungssystem... (Strg+C zum Beenden)")
        ventil_input = input("🔧 Ventil offen? (j/n): ").strip().lower()
        steuerdaten["v104_offen"] = ventil_input == "j"
        print(f"🔁 Ventilstatus gesetzt: {'offen' if steuerdaten['v104_offen'] else 'geschlossen'}")
        sollwert_mm = int(input("🎯 Soll-Füllstand in mm (z. B. 100): ").strip())
        print(f"🎯 Sollwert gesetzt auf {sollwert_mm} mm")
    else:
        print("▶️ Starte Steuerungssystem... (Strg+C zum Beenden)")
        ventil_input = input("🔧 Ventil offen? (j/n): ").strip().lower()
        steuerdaten["v104_offen"] = ventil_input == "j"
        print(f"🔁 Ventilstatus gesetzt: {'offen' if steuerdaten['v104_offen'] else 'geschlossen'}")
        sollwert_mm = int(input("🎯 Soll-Füllstand in mm (z. B. 100): ").strip())
        print(f"🎯 Sollwert gesetzt auf {sollwert_mm} mm")
        plc.connect()
        print("✅ SPS-Verbindung hergestellt")

    reset_log()

    mess_thread = threading.Thread(target=messzyklus, args=(stop_event,), daemon=True)
    mess_thread.start()

    plot_thread = threading.Thread(target=start_live_plot, daemon=True)
    plot_thread.start()

    #schedule.every(1).seconds.do(pumpenzyklus, sollwert_mm)

    try:
        while True:
            schedule.run_pending()
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n🛑 Steuerung beendet durch Benutzer")
        stop_event.set()
        mess_thread.join()  # Warten bis messzyklus Thread sauber endet
        plot_fuellstaende()
        beenden(plc)

