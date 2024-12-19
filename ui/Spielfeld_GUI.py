import pygame
import sys

from Spielfeld import *

class Spielfeld_GUI():
    def __init__(self):
        # Farben definieren
        self.weiss = (255, 255, 255)
        self.schwarz = (0, 0, 0)
        self.rot = (255, 0, 0)
        self.blau = (0, 0, 255)
        self.gruen = (0, 255, 0)
        self.gelb = (255, 255, 0)

        # Spielfeld-Einstellungen
        self.WIDTH, self.HEIGHT = 600, 600  # Fenstergröße
        self.feldgroesse = 40  # Größe der einzelnen Felder
        self.kreisradius = 15  # Radius der Kreise
        self.groesse = 11  # Größe des Spielfelds (11x11 Felder)

        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Mensch ärgere dich nicht")
        

        self.spielfeld = Spielfeld()
        self.spielfeld.erstelleFeld(40)
        # Zugriff auf Figuren der Farbe ...
        # dor = self.figuren['rot']
        # Zugriff auf Farben
        #for figur in dor:
        #    print(figur)

        self.timerStart = 30  # Startzeit in Sekunden
        self.timer = self.timerStart  # Aktueller Timer
        self.font = pygame.font.Font(None, 36)
        
        self.zeit = pygame.time.Clock()
        
        #Startfelder
        self.startfeld = [
            {"farbe": self.rot, "spalte": 0, "reihe": 4},
            {"farbe": self.blau, "spalte": 6, "reihe": 0},
            {"farbe": self.gelb, "spalte": 4, "reihe": 10},
            {"farbe": self.gruen, "spalte": 10, "reihe": 6},
        ]
        

    def run(self):
        """Startet die Hauptspiel-Schleife"""
        letztZeit = pygame.time.get_ticks()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # Maus-Klick
                    feld_pos = self.holeFeld(pygame.mouse.get_pos())
                    if feld_pos:
                        print(f"Feld {feld_pos}")
                    else:
                        print("außerhalb des Spielfeldes")
            
            aktZeit = pygame.time.get_ticks()
            if aktZeit - letztZeit >= 1000:  # 1000 milliseconds = 1 second
                letztZeit = aktZeit
                if self.timer > 0:
                    self.timer -= 1
                else:
                    self.timer = self.timerStart

            self.zeichneBrett()
            self.zeigeTimer()
            #self.spielfeld.platziereFiguren(self.figuren)
            
            #print(self.figuren['rot'][0].holePosition())

            pygame.display.flip()
            
            

    def zeichneBrett(self):
        """Zeichnet das komplette Spielfeld"""
        self.screen.fill(self.weiss)

        # Spielfeld Position berechnen
        self.brett_start_x = (self.WIDTH - self.groesse * self.feldgroesse) / 2
        self.brett_start_y = (self.HEIGHT - self.groesse * self.feldgroesse) / 2
        #print(self.brett_start_x)
        #print(self.brett_start_y)

        # Spielfeld zeichnen
        for reihe in range(self.groesse):
            for spalte in range(self.groesse):
                rect = pygame.Rect(
                    self.brett_start_x + spalte * self.feldgroesse,
                    self.brett_start_y + reihe * self.feldgroesse,
                    self.feldgroesse, self.feldgroesse
                )

                # Laufpfade: Hauptlinien
                for feld in self.spielfeld._SFeld:
                    #print(feld.position)
                    if feld.position == (reihe, spalte):
                        pygame.draw.circle(self.screen, self.schwarz, rect.center, self.kreisradius)
                        pygame.draw.circle(self.screen, self.weiss, rect.center, self.kreisradius-3)


        # Start- und Zielfelder zeichnen
        self.zeichneStartUndZiel()

        self.zeichneFiguren()
        
    def zeigeTimer(self):
        """Zeigt den Countdown-Timer auf dem Bildschirm an"""
        timer_text = self.font.render(f"Zeit übrig: {self.timer}s", True, self.schwarz)
        self.screen.blit(timer_text, (10, 10))

    
    
    def Startfeld(self, spalte, reihe, farbe):
        """Zeichnet individuelle Startfelder mit der zugehörigen Farbe."""
        center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
        center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
        pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

    
    
    def zeichneStartUndZiel(self):
        """Zeichnet Start- und Zielfelder"""
        for farbe, positionen in self.spielfeld.startfelder.items():
            for (reihe, spalte) in positionen:
                self.zeichneStart(spalte, reihe, self.uebersetzeFarbe(farbe))

        for farbe, positionen in self.spielfeld.zielfelder.items():
            for (reihe, spalte) in positionen:
                self.zeichneZiel(spalte, reihe, self.uebersetzeFarbe(farbe))
        

    def zeichneStart(self, spalte, reihe, farbe):
        """Zeichnet Startfelder"""
        center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
        center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
        pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

    def zeichneZiel(self, spalte, reihe, farbe):
        """Zeichnet Zielfelder"""
        center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
        center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
        pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

    def zeichneFiguren(self):
        """Zeichnet die Figuren auf ihren aktuellen Positionen"""
        pass


    def holePosition(self):
        pass

    def uebersetzeFarbe(self, farbe):
        """gibt die Farbe als globale Variable zurück"""
        farben = {
            'rot': self.rot,
            'blau': self.blau,
            'gelb': self.gelb,
            'gruen': self.gruen,
        }
        return farben.get(farbe, self.schwarz)

    def holeFeld(self, maus_pos):
        """Gibt die Feldposition (reihe, spalte) zurück anhand der GUI
            Hinweis: holt nur alle Felder außer Start- und Zielfelder
        """
        x, y = maus_pos

        # Berechnung der Feldkoordinaten
        spalte = int((x - self.brett_start_x) // self.feldgroesse)
        reihe = int((y - self.brett_start_y) // self.feldgroesse)

        # Überprüfung ob die berechnete Position innerhalb des Spielfeldes liegt
        if 0 <= spalte < self.groesse and 0 <= reihe < self.groesse:
            for feld in self.spielfeld._SFeld:
                if feld.holePosition() == (reihe, spalte):
                    if feld.ist_start == True:
                        print("STARTFELD")
                        print(feld.farbe)
                    elif feld.ist_ziel == True:
                        print("ZIELFELD")
                        print(feld.farbe)
                    return reihe, spalte
        else:
            return None  # Maus war außerhalb des Spielfeldes


if __name__ == "__main__":
    spielfeld = Spielfeld_GUI()
    spielfeld.run()
    self.zeit.tick(30)
