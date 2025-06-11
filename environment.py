

TESTMODUS= True


class Behaelter:
    def __init__(self, name, fuellstand, maxstand,minstand):
        self.name = name
        self.fuellstand = fuellstand
        self.maxstand = maxstand
        self.minstand = minstand

    def fuellen(self, menge):
        self.fuellstand += menge
        if self.fuellstand > self.maxstand:
            self.fuellstand = self.maxstand

    def entleeren(self, menge):
        self.fuellstand -= menge
        if self.fuellstand < 0:
            self.fuellstand = 0

    def __repr__(self):
        prozent = self.fuellstand / self.maxstand * 100
        return f"{self.name}: {self.fuellstand:.1f} mm ({prozent:.1f}%)"
"""
sensorwerte = {
    "fuellstand_b101": 0.0,
    "fuellstand_b102": 0.0,
}
"""

steuerdaten = {
    "letzter_pumpenwert": 0,
    "sollwert": 100,
    "v104_offen": False
}

b101 = Behaelter("B101", 300.0, 300.0,142.0)
b102 = Behaelter("B102", 20.0, 178.0,20.0)
