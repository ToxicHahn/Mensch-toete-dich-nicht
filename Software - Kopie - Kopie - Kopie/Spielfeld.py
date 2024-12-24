from Feld import *
from Farbfeld import *
from Figur import *
from Wuerfel import *
from random import * 
from PyQt5.QtCore import QTimer

class Spielfeld:
    def __init__(self):
        self._SFeld = []  # Hauptspielfeld
        self.startFeld = []
        self.zielFeld = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.checkNaechsteFigur)
        self.schritte = None

        self.wuerfel = Wuerfel()

        self.zeit = True # True: Zeit läuft, False Zeit stoppt

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
        
        # Zuweisung der Positionen der Figuren
        for farbe, positionen in self.startfelder.items():
            for i, position in enumerate(positionen):
                self.figuren[farbe][i].setzePosition(position)
        
        # erste Figur, die sich bewegt: also die erste rote Figur
        self.naechsteFigur = self.figuren["rot"][0]
    
    # Getter und Setter
    def setzeNaechsteFigur(self, figur):
        self.naechsteFigur = figur

    def holeNaechsteFigur(self):
        return self.naechsteFigur
    
    def holeZeit(self):
        return self.zeit
    
    def setzeZeit(self, x):
        self.zeit = x

    def holeAktiv(self):
        return self.wuerfel.aktiv

    # Erstelle das Feld; Anpassung mit Mapskin nötig
    def erstelleFeld(self, n: int):
        """Erstellt ein Feld der geforderten Groesse"""
        for i in range(n):
            self._SFeld.append(Feld(i+1, None))

        """Definiert die Pfadfelder (Positionen der weißen Kreise)"""
        pfad_coords = [
            (0,4), (0,5), (0,6), (1,6), (2,6),
            (3,6), (4,6), (4,7), (4,8), (4,9),
            (4,10), (5,10), (6,10), (6,9), (6,8),
            (6,7), (6,6), (7,6), (8,6), (9,6),
            (10,6), (10,5), (10,4), (9,4), (8,4),
            (7,4), (6,4), (6,3), (6,2), (6,1),
            (6,0), (5,0), (4,0), (4,1), (4,2), (4,3),
            (4,4), (3,4), (2,4), (1,4),
        ]

        # Zuweisung der Feldpositionen
        for i, feld in enumerate(self._SFeld):
            if i < len(pfad_coords):
                reihe, spalte = pfad_coords[i]
                feld.setzePosition((reihe, spalte))

        # Zuordnung der Farbfeldern
        farben = ["rot", "blau", "gelb", "gruen"]
        for farbe in farben:
            # Startfelder
            for position in self.startfelder[farbe]:
                farbfeld = Farbfeld(farbe, (position[0],position[1]), ist_start=True)
                self.startFeld.append(farbfeld)
                # self._SFeld.append(farbfeld)

            # Zielfelder
            for position in self.zielfelder[farbe]:
                farbfeld = Farbfeld(farbe, (position[0], position[1]), ist_ziel=True)
                self.zielFeld.append(farbfeld)
                # self._SFeld.append(farbfeld)

    def bewegeFigur(self, figur, schritte):
        """Bewege eine Figur mit einer bestimmten Anzahl an Schritten """
        aktPos = figur.holePosition()
        if figur.holeRaus() == False:
            if schritte != 1: # Sobald man keine 1 würfelt, kommt man nicht raus
                return
            else:
                # 1. Mal Bewegen einer Figur
                figur.setzeRaus()
                for position in self.startfelder['rot']:
                    if aktPos == position:
                        figur.setzePosition((4,0))
                        return
        else:
            if schritte == 1:
                print("Wähle eine Figur aus")
                self.wuerfel.deaktivieren()
                self.zeit=False
                self.warte()
                if self.holeNaechsteFigur() is not None:
                    print("FIGUR")
                    self.wuerfel.aktivieren()
                    for position in self.startfelder['rot']:
                        if self.holeNaechsteFigur().holePosition() == position:
                            print("IST STARTFELD")
                            self.holeNaechsteFigur().setzePosition((4,0))
                        else:
                            print("KEIN STARTFELD")
                            self.weitergehts(figur)
                    self.zeit=True
                    return
                
                print("KEINE FIGUR")

            self.weitergehts(figur)
        




        """


        aktPos = figur.holePosition()
        farbe = figur.holeFarbe()
        if figur.holeRaus() == False:
            if schritte != 1:
                return
            else:
                figur.setzeRaus()
                start_position = self.startfelder[farbe][0]
                figur.setzePosition(start_position)
        else:
            if schritte == 1:
                print("Wähle eine Figur aus")
                self.wuerfel.deaktivieren()
                self.zeit=False
                self.warte()
            else:
                feld_generator = (feld for feld in self._SFeld if feld.holePosition() == aktPos)
            try:
                aktFeld = next(feld_generator)
                aktIndex = self._SFeld.index(aktFeld)
            except StopIteration:
                print("Kein Feld mit der aktuellen Position gefunden!")  # Debugging-Ausgabe
                return

            neuIndex = (aktIndex + schritte) % len(self._SFeld)
            neuesFeld = self._SFeld[neuIndex]

            if neuesFeld.istFrei():
                self._SFeld[aktIndex].verlassen()
                neuesFeld.betreten(figur)
                figur.setzePosition(neuesFeld.holePosition())
            else:
                print("Feld ist bereits besetzt!")

            """
    def weitergehts(self, figur):
        schritte = self.wuerfel.holeZahl()
        aktPos = figur.holePosition()

        
        if self.holeNaechsteFigur() is not None:
            for position in self.startfelder['rot']:
                if self.holeNaechsteFigur().holePosition() == position:
                    print("IST STARTFELD")
                    self.holeNaechsteFigur().setzePosition((4,0))
                    return
        else:
            aktIndex = self._SFeld.index(next(feld for feld in self._SFeld if feld.holePosition() == aktPos))
            print(aktIndex)
                    
            new_index = (aktIndex + schritte) % len(self._SFeld)
            print(aktIndex, new_index, schritte, len(self._SFeld))
            if new_index >= 39:
                new_index - 39
            new_feld = self._SFeld[new_index]
                    
            if new_feld.istFrei():
                self._SFeld[aktIndex].verlassen()
                new_feld.betreten(figur)
            else:
                print("Feld ist bereits besetzt!")

            figur.setzePosition(new_feld.holePosition())
                


    def verfuegbareFiguren(self, farbe):
        """Gibt eine Liste der verfügbaren Figuren einer bestimmten Farbe zurück"""
        return [figur for figur in self.figuren[farbe] if figur.holeRaus()]
   
    def warte(self):
        """Waits for the next figure to be selected"""
        print("Waiting for next figure to be selected...")
        self.timer.start(100)  # Überprüfe alle 100 ms

    def checkNaechsteFigur(self):
        if self.holeNaechsteFigur() is not None:
            self.timer.stop()
            self.weiter(self.holeNaechsteFigur())
        
    
    def weiter(self, figur):
        if self.holeNaechsteFigur() is not None:
            print("FIGUR")
            self.wuerfel.aktivieren()
            for position in self.startfelder['rot']:
                        if self.holeNaechsteFigur().holePosition() == position:
                            print("IST STARTFELD")
                            self.holeNaechsteFigur().setzePosition((4,0))
                        else:
                            print("KEIN STARTFELD")
                            self.weitergehts(figur)
            self.zeit=True
            self.wuerfel.aktivieren()
            return
        self.weitergehts(figur)
        
    

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
