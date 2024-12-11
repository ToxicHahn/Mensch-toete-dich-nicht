class Feld():
    def __init__(self, effekt=None):
        self.effekt = effekt
        self.besetzt = False
    def setzeEffekt(self, effekt):
        self.effekt = effekt
    def holeEffekt(self):
        return self.effekt
    def istBesetzt(self):
        return self.besetzt
    def feldBesetzen(self):
        self.besetzt = True
    def feldVerlassen(self):
        self.besetzt = False