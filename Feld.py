class Feld():
    def __init__(self, effekt=None):
        self.effekt = effekt
        self.besetzt: bool = False
    def setzeEffekt(self, effekt):
        """Setzt einen Effekt fest"""
        self.effekt = effekt
    def holeEffekt(self):
        """Returned den aktuell gesetzten Effekt"""
        return self.effekt
    def istBesetzt(self):
        """Returned Besetzung Status
         False = Leeres Feld
         True = Besetzes Feld"""
        return self.besetzt
    def besetzen(self):
        """Setzt dieses Feld auf besetzt"""
        self.besetzt = True
    def verlassen(self):
        """Setzt dieses Feld auf leer"""
        self.besetzt = False