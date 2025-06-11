import environment

def simuliere_behaelter():
    zykluszeit = 2
    k = 0.0001071

    pumpe_aktiv = environment.steuerdaten["letzter_pumpenwert"] > 7000
    rueckfluss_aktiv = not pumpe_aktiv

    if pumpe_aktiv:
        menge = environment.steuerdaten["letzter_pumpenwert"] * k * zykluszeit
        environment.b101.entleeren(menge)
        environment.b102.fuellen(menge)

    elif rueckfluss_aktiv:
        if environment.sensorwerte["v104_offen"]:
            druckfaktor = (environment.b102.fuellstand - 20) / (178 - 20)
            rueckflussrate = 0.4 + druckfaktor * 1.2
        else:
            rueckflussrate = 0.4

        rueckfluss = rueckflussrate * zykluszeit
        environment.b101.fuellen(rueckfluss)
        environment.b102.entleeren(rueckfluss)

    environment.b101.fuellstand = round(max(136, min(environment.b101.fuellstand, 300)), 1)
    environment.b102.fuellstand = round(max(20, min(environment.b102.fuellstand, 178)), 1)

    environment.sensorwerte["fuellstand_b101"] = environment.b101.fuellstand
    environment.sensorwerte["fuellstand_b102"] = environment.b102.fuellstand

    print(environment.b101)
    print(environment.b102)
