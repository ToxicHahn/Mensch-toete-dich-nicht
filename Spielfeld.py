from Feld import *
from Farbfeld import *
from Figur import *
from Wuerfel import *
from random import * 

class Spielfeld():
    def __init__(self):
        self._SFeld = []  # Hauptspielfeld
        self.startFeld = []
        self.zielFeld = []

        self.startfelder = {
            "rot": [(0,0),(0,1),(1,0),(1,1)],
            "blau": [(0,9),(0,10),(1,9),(1,10)],
            "gelb": [(9,0),(9,1),(10,0),(10,1)],
            "gruen": [(9,9),(9,10),(10,9),(10,10)],
        }  # Startfelder pro Farbe

        self.zielfelder = {
            "rot": [(5,1),(5,2),(5,3),(5,4)],
            "blau": [(1,5),(2,5),(3,5),(4,5)],
            "gelb": [(6,5),(7,5),(8,5),(9,5)],
            "gruen": [(5,6),(5,7),(5,8),(5,9)],
        }  # Zielfelder pro Farbe

        self.figuren = {
            "rot": [Figur("rot", i) for i in range(4)],
            "blau": [Figur("blau", i) for i in range(4)],
            "gelb": [Figur("gelb", i) for i in range(4)],
            "gruen": [Figur("gruen", i) for i in range(4)],
        }

        #print(len(self.felder))

        # for farbe in ["rot", "blau", "gelb", "gruen"]:
        #     self.startfelder[farbe] = [Farbfeld(i, farbe, ist_start=True) for i in range(4)]
        #     self.zielfelder[farbe] = [Farbfeld(i, farbe, ist_ziel=True) for i in range(4)]

    def holeFeld(self, nummer):
        pass
    
    def bewegeFigur(self, figur, spalte, reihe):
        """Platziert Figuren auf ihren Startfeldern"""
        for felder in self._SFeld:
            if felder.position == (reihe, spalte): 
                feld = felder   # Position des gewollten Feldes

        if feld.besetzt is None:  # Nur platzieren, wenn das Feld leer ist
            feld.besetztVon = figur  # Figur auf das Feld setzen
            if not figur.imZielFrage:
                figur.setzePosition((spalte, reihe))  # Position der Figur aktualisieren
        else:
            print("Feld ist bereits besetzt!")

    def erstelleFeld(self, n: int):
        """Erstellt ein Feld der geforderten Groesse"""
        for i in range(n):
            self._SFeld.append(Feld(i+1, None))

        """Definiert die Pfadfelder (Positionen der weißen Kreise)"""
        pfad_coords = [
            (0,4), (0,5), (0,6), (1,4), (1,6),
            (2,4), (2,6), (3,4), (3,6), (4,0),
            (4,1), (4,2), (4,3), (4,4), 
            (4,6), (4,7), (4,8), (4,9),
            (4,10), (5,0), (5,10), (6,0),
            (6,1), (6,2), (6,3), (6,4),
            (6,6), (6,7), (6,8), (6,9), (6,10),
            (7,4), (7,6), (8,4), (8,6),
            (9,4), (9,6), (10,4), (10,5), (10,6)
        ]

        for i, feld in enumerate(self._SFeld):
            if i < len(pfad_coords):
                reihe, spalte = pfad_coords[i]
                feld.setzePosition((reihe, spalte))

        farben = ["rot", "blau", "gelb", "gruen"]

        for farbe in farben:
            # Startfelder
            for position in self.startfelder[farbe]:
                farbfeld = Farbfeld(farbe, (position[0],position[1]), ist_start=True)
                # self.startFeld.append(farbfeld)
                self._SFeld.append(farbfeld)

            # Zielfelder
            for position in self.zielfelder[farbe]:
                farbfeld = Farbfeld(farbe, (position[0], position[1]), ist_ziel=True)
                # self.zielFeld.append(farbfeld)
                self._SFeld.append(farbfeld)
   
    
    def EffekteEinfuegen(self, l: list[tuple[int, str]]):
        """Fuegt die Effekte in die Felder des Spielfelds ein"""
        for (i,e) in l:
            self._SFeld[i].setzeEffekt(e)

    def Effekte(self):
        """Definition der Effekte"""
        self.E = []
    
    def gibEffekt(self, k: int) -> str:
        """Gibt einen Effekt zurueck"""
        return self.E[k]

    def randomEffekt(self) -> str:
        """Gibt einen zufaelligen Effekt zurueck"""
        return self.gibEffekt(randint(0,len(self.E)-1))

    def randomEffekteErstellen(self, n: int = 0):
        """Erstellt zufaellige Effekte fuer das Spielfeld und fuegt sie ein"""
        if not n:
            n = randint(0,len(self._SFeld)-1)
        l = []
        for i in range(n):
            r = randint(0,len(self._SFeld)-1)
            if not any(r in tupel for tupel in l):
                l += (r, self.randomEffekt())
        self.EffekteEinfuegen(l)
