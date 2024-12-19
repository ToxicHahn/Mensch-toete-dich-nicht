class Feld():
    def __init__(self, nummer, position, ist_start=False, ist_ziel=False, ):
        self.nummer = nummer
        self.position = position
        self.ist_start = ist_start
        self.ist_ziel = ist_ziel
        self.besetztVon = None  # Figur, die sich aktuell auf diesem Feld befindet

    def istFrei(self):
        return self.besetztVon is None

    def betreten(self, figur):
        if self.istFrei():
            self.besetztVon = figur
            figur.position = self.position
            return True
        return False

    def verlassen(self):
        self.besetztVon = None

    def setzePosition(self, position):
        self.position = position

    def holePosition(self):
        return self.position
        
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