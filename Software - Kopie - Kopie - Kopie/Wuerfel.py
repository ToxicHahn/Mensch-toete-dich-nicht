import random

class Wuerfel():
    def __init__(self):
        self._zahl=0
        self.gewuerfelt = False
        self.aktiv = True
    def rollen(self):
        self._zahl = random.randint(1,6)
    def holeZahl(self):
        return self._zahl
    
    def hatGewuerfelt(self):
        return self.gewuerfelt
    
    def setzeHatGewuerfelt(self, x):
        self.gewuerfelt = x

    def aktivieren(self):
        self.aktiv = True

    def deaktivieren(self):
        self.aktiv = False

class negWuerfel():
    def __init__(self):
        self._negzahl:int = None
    def negRollen(self):
        self._negzahl = random.randint(-1,-6)
    def holeNegZahl(self):
        return self._negzahl