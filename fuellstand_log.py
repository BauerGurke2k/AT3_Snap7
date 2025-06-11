import csv
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---- Logging ----

from sensoren import sensorwerte
import os

def reset_log():
    import csv
    with open("log_fuellstand.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Zeit", "B101 [mm]", "B102 [mm]"])
    print("🧹 log_fuellstand.csv wurde zurückgesetzt.")


def log_fuellstaende():
    try:
        with open("log_fuellstand.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                round(sensorwerte["fuellstand_b101"], 1),
                round(sensorwerte["fuellstand_b102"], 1)
            ])
    except Exception as e:
        print(f"⚠️ Fehler beim Loggen der Füllstände: {e}")

# ---- Statischer Plot (bei Programmende) ----

def plot_fuellstaende():
    zeiten = []
    b101 = []
    b102 = []

    try:
        with open("log_fuellstand.csv", mode="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) < 3:
                    continue
                zeit = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                zeiten.append(zeit)
                b101.append(float(row[1]))
                b102.append(float(row[2]))

        # Zeit in Sekunden relativ zur ersten Messung
        startzeit = zeiten[0]
        sekunden = [(z - startzeit).total_seconds() for z in zeiten]

        plt.plot(sekunden, b101, label="B101")
        plt.plot(sekunden, b102, label="B102")
        plt.xlabel("Vergangene Zeit [s]")
        plt.ylabel("Füllstand [mm]")
        plt.title("Füllstandsverlauf der Behälter")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"⚠️ Fehler beim Plotten: {e}")

# ---- Live-Plot (parallel während Laufzeit) ----

import threading

def start_live_plot():
    thread = threading.Thread(target=_run_live_plot, daemon=True)
    thread.start()

def _run_live_plot():
    fig, ax = plt.subplots()

    def lese_daten():
        zeiten, b101, b102 = [], [], []
        try:
            with open("log_fuellstand.csv", mode="r") as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) != 3:
                        continue
                    zeit = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    zeiten.append(zeit)
                    b101.append(float(row[1]))
                    b102.append(float(row[2]))
        except:
            pass
        return zeiten, b101, b102

    def update_plot(frame):
        zeiten, b101, b102 = lese_daten()
        ax.clear()
        ax.plot(zeiten, b101, label="B101")
        ax.plot(zeiten, b102, label="B102")
        ax.set_title("Live-Füllstände")
        ax.set_xlabel("Zeit")
        ax.set_ylabel("Füllstand [mm]")
        ax.legend()
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

    ani = animation.FuncAnimation(
    fig,
    update_plot,
    interval=2000,
    cache_frame_data=False  # <- Warnung vermeiden
)

    plt.show()
