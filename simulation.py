from environment import steuerdaten,b101,b102


pumpenkonstante = 175.175
k = 0.022142857 #Sensorkalibrierung umrechnung sensorwert in mm
zykluszeit_sim = 1
abflusskonstante = 37.997


rueckflussrate = None
fuellstand_real = 0
fuellstand_sim = 0

def simuliere_behaelter():
    from sensoren import median_mess,median_sim,zykluszeit_mess
    from regelung import motordrehzahl,max_pumpendrehzahl

    global fuellstand_real
    global fuellstand_sim
    global rueckflussrate


    

    pumpe_aktiv = steuerdaten["letzter_pumpenwert"] > 7000
    rueckfluss_aktiv = not pumpe_aktiv

    # Neue Umrechnung: 11000 → 20 mm, 18500 → 178 mm
    skala = (b102.maxstand-b102.minstand)/(18000-11500)
    fuellstand_real = (median_mess - 11000) * skala + 20

#simulierten fülllstand berechnen
    



    menge = pumpenkonstante * (motordrehzahl / max_pumpendrehzahl) * zykluszeit_sim * k
    

    if pumpe_aktiv:
        
        b101.entleeren(menge)
        b102.fuellen(menge)

    elif rueckfluss_aktiv:
        if steuerdaten["v104_offen"]:
            druckfaktor = (b102.fuellstand - 20) / (178 - 20)
            rueckflussrate = 0.4 + druckfaktor * 1.2
        else:
            rueckflussrate = abflusskonstante * k * zykluszeit_sim

        rueckfluss = rueckflussrate * zykluszeit_sim
        b101.fuellen(rueckfluss)
        b102.entleeren(rueckfluss)


#sicherstellen dass max und minwerte nie überschritten werden
    b101.fuellstand = round(max(136, min(b101.fuellstand, 300)), 1)
    b102.fuellstand = round(max(20, min(b102.fuellstand, 178)), 1)

    print(b101)
    print(b102)
    print(f"sim{fuellstand_sim},real{fuellstand_real}")


