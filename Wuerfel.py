import random
class Wuerfel():
    def __init__(self):
        self._zahl:int = None
    def rollen(self):
        self._zahl = random.randint(1,6)
    def holeZahl(self):
        return self._zahl

class negWuerfel():
    def __init__(self):
        self._negzahl:int = None
    def negRollen(self):
        self._negzahl = random.randit(-1,-6)
    def holeNegZahl(self):
        return self._negzahl