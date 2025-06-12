from environment import steuerdaten,b101,b102



k = 0.00001071 #Pumpenkonstante
zykluszeit = 1

def simuliere_behaelter():
    from sensoren import rohwert_median
    from regelung import ansteuerung

    

    pumpe_aktiv = steuerdaten["letzter_pumpenwert"] > 7000
    rueckfluss_aktiv = not pumpe_aktiv

    # Neue Umrechnung: 11000 → 20 mm, 18500 → 178 mm
    skala = 158 / (18500 - 11000)
    fuellstand_mm = (rohwert_median - 11000) * skala 



    if pumpe_aktiv:
        menge = fuellstand_mm
        b101.entleeren(menge)
        b102.fuellen(menge)

    elif rueckfluss_aktiv:
        if steuerdaten["v104_offen"]:
            druckfaktor = (b102.fuellstand - 20) / (178 - 20)
            rueckflussrate = 0.4 + druckfaktor * 1.2
        else:
            rueckflussrate = 5

        rueckfluss = rueckflussrate * zykluszeit
        b101.fuellen(rueckfluss)
        b102.entleeren(rueckfluss)


#sicherstellen dass max und minwerte nie überschritten werden
    b101.fuellstand = round(max(136, min(b101.fuellstand, 300)), 1)
    b102.fuellstand = round(max(20, min(b102.fuellstand, 178)), 1)

    print(b101)
    print(b102)
    print(f"{steuerdaten['letzter_pumpenwert'], rohwert_median}")


