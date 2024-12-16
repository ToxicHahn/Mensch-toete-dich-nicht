import pygame
import sys

class Spielfeld:
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

        # Startpunkte
        self.startpunkte = [
            {"farbe": self.rot, "spalte": 0, "reihe": 0},
            {"farbe": self.blau, "spalte": 9, "reihe": 0},
            {"farbe": self.gelb, "spalte": 0, "reihe": 9},
            {"farbe": self.gruen, "spalte": 9, "reihe": 9},
        ]
        
        self.startfeld = [
            {"farbe": self.rot, "spalte": 0, "reihe": 4},
            {"farbe": self.blau, "spalte": 6, "reihe": 0},
            {"farbe": self.gelb, "spalte": 4, "reihe": 10},
            {"farbe": self.gruen, "spalte": 10, "reihe": 6},
        ]

    def run(self):
        """Startet die Hauptspiel-Schleife"""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.zeichneBrett()
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
                if self.pfad(reihe, spalte):
                    pygame.draw.circle(self.screen, self.schwarz, rect.center, self.kreisradius)
                    pygame.draw.circle(self.screen, self.weiss, rect.center, self.kreisradius-3)


        # Start- und Zielfelder zeichnen
        self.zeichneStartUndZiel()

    def pfad(self, reihe, spalte):
        """Definiert die Pfadfelder (Positionen der weißen Kreise)"""
        pfad_coords = [
            (0,4), (0,5), (1,4), (1,6),
            (2,4), (2,6), (3,4), (3,6),
            (4,1), (4,2), (4,3), (4,4), 
            (4,6), (4,7), (4,8), (4,9),
            (4,10), (5,0), (5,10), (6,0),
            (6,1), (6,2), (6,3), (6,4),
            (6,6), (6,7), (6,8), (6,9),
            (7,4), (7,6), (8,4), (8,6),
            (9,4), (9,6), (10,5), (10,6)
        ]
        return (reihe, spalte) in pfad_coords
    
    def Startfeld(self, spalte, reihe, farbe):
        """Zeichnet individuelle Startfelder mit der zugehörigen Farbe."""
        center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
        center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
        pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

    
    def zeichneStartUndZiel(self):
        """Zeichnet Start- und Zielfelder"""
        for feld in self.startpunkte:
            self.zeichneStart(feld["spalte"], feld["reihe"], feld["farbe"])

        for feld in self.startfeld:
            self.Startfeld(feld["spalte"], feld["reihe"], feld["farbe"])
        
        
        # Zielfelder
        self.zeichneZiel(self.rot, "horizontal", (5, 1))
        self.zeichneZiel(self.blau, "vertikal", (1, 5))
        self.zeichneZiel(self.gelb, "vertikal", (6, 5))
        self.zeichneZiel(self.gruen, "horizontal", (5, 6))

    def zeichneStart(self, start_spalte, start_reihe, farbe):
        """Zeichnet die 4 Startfelder als farbige Kreise"""
        for i in range(2):
            for j in range(2):
                center_x = self.brett_start_x + (start_spalte + i) * self.feldgroesse + self.feldgroesse / 2
                center_y = self.brett_start_y + (start_reihe + j) * self.feldgroesse + self.feldgroesse / 2
                pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

    def zeichneZiel(self, farbe, orientation, start):
        """Zeichnet die Zielfelder."""
        reihe, spalte = start
        for i in range(4):
            if orientation == "horizontal":
                center_x = self.brett_start_x + (spalte + i) * self.feldgroesse + self.feldgroesse / 2
                center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
            else:
                center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
                center_y = self.brett_start_y + (reihe + i) * self.feldgroesse + self.feldgroesse / 2
            pygame.draw.circle(self.screen, farbe, (center_x, center_y), self.kreisradius)

if __name__ == "__main__":
    spielfeld = Spielfeld()
    spielfeld.run()
