class Figur:
    def __init__(self, farbe, zahl, position=None, raus = False):
        self.farbe = farbe
        self.zahl = zahl
        self.position = position  # Aktuelle Position der Figur
        self.raus = raus
        self.imZiel = False  # Status, ob die Figur das Ziel erreicht hat

    def bewege(self, felder):
        if self.im_ziel:
            return
        self.position = felder

    def setzePosition(self, position):
        self.position = position
    
    def holePosition(self):
        return self.position
    
    def setzeRaus(self):
        self.raus = True

    def holeRaus(self):
        return self.raus
    
    def setzeFarbe(self, farbe):
        self.farbe = farbe

    def holeFarbe(self):
        return self.farbe

    def setze_auf_start(self, startfeld):
        self.position = startfeld

    def erreiche_ziel(self):
        self.imZiel = True
    
    def imZielFrage(self):
        if self.imZiel == True:
            return True
        return False
