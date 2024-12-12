from Feld import *
from random import * 
class Spielfeld():
    def __init__(self, n):
        self.SFeld = []
        self.erstelleFeld(n)
    
    def erstelleFeld(self, n):
        """Erstellt ein Feld der geforderten Groesse"""
        for i in range(n):
            self.SFeld.append(Feld())
    
    def gibEffekte(self, l):
        """Fuegt die Effekte in die Felder des Spielfelds ein"""
        for (i,e) in l:
            self.SFeld[i].setzeEffekt(e)

    def Effekte(self):
        """Definiert die Effekte"""
        self.E = {
            "E1": "",
            "E2": "",
            "E3": "",
            "E4": "",
            "E5": "",
            "E6": ""}
    
    def gibEffekt(self, k):
        """Gibt einen Effekt zurueck"""
        return self.E[k]

    def randomEffekt(self):
        """Gibt einen zufaelligen Effekt zurueck"""
        return self.gibEffekt[f"E{randint(1,len(self.E))}"]

    def randomEffekteVerteilen(self, n=0):
        """Erstellt zufaellige Effekte fuer das Spielfeld und fuegt sie ein"""
        if not n:
            n = randint(0,len(self.SFeld)-1)
        l = []
        for i in range(n):
            r = randint(0,len(self.SFeld)-1)
            if not any(r in tupel for tupel in l):
                l += (r, self.randomEffekt())
        
        self.gibEffekte(l)
                
                
        
#    def bewegen(self, Figur)
        
    
