import csv
from datetime import datetime
import matplotlib.pyplot as plt
from environment import b101,b102

def reset_log():
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
                round(b101.fuellstand, 1),
                round(b102.fuellstand, 1)
            ])
        #print(f"wird geloggt")
    except Exception as e:
        print(f"⚠️ Fehler beim Loggen der Füllstände: {e}")

def plot_fuellstaende():
    zeiten, b101, b102 = [], [], []

    try:
        with open("log_fuellstand.csv", "r") as file:
            reader = csv.reader(file)
            next(reader)  # Header überspringen
            for row in reader:
                if len(row) < 3:
                    continue
                try:
                    zeit = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                    b101_wert = float(row[1])
                    b102_wert = float(row[2])
                except Exception:
                    continue
                zeiten.append(zeit)
                b101.append(b101_wert)
                b102.append(b102_wert)

        if not zeiten:
            print("Keine Daten zum Plotten gefunden.")
            return

        startzeit = zeiten[0]
        sekunden = [(z - startzeit).total_seconds() for z in zeiten]

        plt.figure()
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

# --- Live-Plot mit interaktivem Modus ---

def start_live_plot(pause_interval=2):
    plt.ion()  # Interaktiver Modus an
    fig, ax = plt.subplots()

    def lese_daten():
        zeiten, b101, b102 = [], [], []
        try:
            with open("log_fuellstand.csv", "r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if len(row) != 3:
                        continue
                    try:
                        zeit = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                        b101_wert = float(row[1])
                        b102_wert = float(row[2])
                    except Exception:
                        continue
                    zeiten.append(zeit)
                    b101.append(b101_wert)
                    b102.append(b102_wert)
        except Exception:
            pass
        return zeiten, b101, b102

    while True:
        zeiten, b101, b102 = lese_daten()
        ax.clear()
        if not zeiten:
            ax.text(0.5, 0.5, "Keine Daten zum Anzeigen", ha="center", va="center", fontsize=14)
        else:
            ax.plot(zeiten, b101, label="B101")
            ax.plot(zeiten, b102, label="B102")
            ax.set_title("Live-Füllstände")
            ax.set_xlabel("Zeit")
            ax.set_ylabel("Füllstand [mm]")
            ax.legend()
            ax.grid(True)
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
            plt.tight_layout()
        plt.pause(pause_interval)  # Aktualisiere das Fenster alle pause_interval Sekunden
