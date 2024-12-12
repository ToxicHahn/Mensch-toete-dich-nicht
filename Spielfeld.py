from Feld import *
from random import * 
from typing import List, Tuple

class Spielfeld():
    def __init__(self, n: int):
        self.SFeld = []
        self.erstelleFeld(n)
    
    def erstelleFeld(self, n: int):
        """Erstellt ein Feld der geforderten Groesse"""
        for i in range(n):
            self.SFeld.append(Feld())
    
    def EffekteEinfuegen(self, l: list[Tuple[int, str]]):
        """Fuegt die Effekte in die Felder des Spielfelds ein"""
        for (i,e) in l:
            self.SFeld[i].setzeEffekt(e)

    def Effekte(self):
        """Definition der Effekte"""
        self.E = []
    
    def gibEffekt(self, k: int) -> str:
        """Gibt einen Effekt zurueck"""
        return self.E[k]

    def randomEffekt(self) -> str:
        """Gibt einen zufaelligen Effekt zurueck"""
        return self.gibEffekt(randint(0,len(self.E)-1))

    def randomEffekteErstellen(self, n = 0):
    """Erstellt zufaellige Effekte fuer das Spielfeld und fuegt sie ein"""
        if not n:
            n = randint(0,len(self.SFeld)-1)
        l = []
        for i in range(n):
            r = randint(0,len(self.SFeld)-1)
            if not any(r in tupel for tupel in l):
                l += (r, self.randomEffekt())
        self.EffekteEinfuegen(l)
