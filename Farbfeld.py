from Feld import Feld

class Farbfeld(Feld):
    def __init__(self, farbe, position, ist_start=False, ist_ziel=False):
        super().__init__(None, None, ist_start, ist_ziel)
        self.farbe = farbe
        self.position = position

    def istFreundlich(self, figur):
        return self.farbe == figur.farbe

    def betreten(self, figur):
        if self.istFreundlich(figur):
            return super().betreten(figur)
        return False  # Gegnerische Figuren dürfen dieses Feld nicht betreten
