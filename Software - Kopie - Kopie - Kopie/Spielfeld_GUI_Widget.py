import sys
import pygame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPainter, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication
from Spielfeld import Spielfeld

class PygameWidget(QWidget):
    def __init__(self, spielfeld, wuerfelWidget, parent=None):
        super().__init__(parent)
        self.spielfeld = spielfeld
        self.wuerfelwidget = wuerfelWidget
        self.setFixedSize(600, 600)
        self.initPygame()
        self.timer = QTimer(self)
        
        # Update der GUI
        self.timer.timeout.connect(self.aktualisierePygame)
        self.timer.start(16) 

    def initPygame(self):
        pygame.init()
        self.screen = pygame.Surface((600, 600))
        self.spielfeld_gui = Spielfeld_GUI(self.spielfeld, self.wuerfelwidget, self.screen)

    def paintEvent(self, event):
        # Pygame in PyQt
        qt_image = self.uebersetzePygameInPyQT(self.screen)
        painter = QPainter(self)
        painter.drawImage(0, 0, qt_image)

    def uebersetzePygameInPyQT(self, surface):
        w, h = surface.get_size()
        data = surface.get_buffer().raw
        qt_image = QImage(data, w, h, QImage.Format_RGB32)
        return qt_image

    def aktualisierePygame(self,):
        self.spielfeld_gui.run()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        pos = (event.x(), event.y())
        self.spielfeld_gui.Mausklick(pos)
        # self.update()

    def reset_timer(self):
        self.spielfeld_gui.reset_timer()

class Spielfeld_GUI():
    def __init__(self, spielfeld, wuerfel, screen):
        # Farben definieren
        self.weiss = (255, 255, 255)
        self.schwarz = (0, 0, 0)
        self.rot = (255, 0, 0)
        self.blau = (0, 0, 255)
        self.gruen = (0, 255, 0)
        self.gelb = (255, 255, 0)
        self.hellblau = (173, 216, 230)

        self.spielfeld = spielfeld
        self.wuerfelw = wuerfel

        # Spielfeld-Einstellungen
        self.WIDTH, self.HEIGHT = 600, 600  # Fenstergröße
        self.feldgroesse = 40  # Größe der einzelnen Felder
        self.kreisradius = 15  # Radius der Kreise
        self.groesse = 11  # Größe des Spielfelds (11x11 Felder)

        self.screen = screen

        self.spielfeld.erstelleFeld(40)

        self.timerStart = 10  # Startzeit in Sekunden
        self.timer = self.timerStart  # Aktueller Timer
        self.zeit = pygame.time.Clock()
        self.letztZeit = pygame.time.get_ticks()

        self.font = pygame.font.SysFont('verdana', 24)
        
        # Startfelder (nur für das Design)
        self.startfeld = {
            "rot": [(4,0)],
            "blau": [(0,6)],
            "gelb": [(10,4)],
            "gruen": [(6,10)],
        }

        self.figurenBilder = {
            'rot': pygame.image.load('Spielfigur_Rot.png'),
            'blau': pygame.image.load('Spielfigur_Blau.png'),
            'gelb': pygame.image.load('Spielfigur_Gelb.png'),
            'gruen': pygame.image.load('Spielfigur_Gruen.png'),
        }
        self.angeklicktesFeld = None

        for i in self.figurenBilder:
            self.figurenBilder[i] = pygame.transform.scale(self.figurenBilder[i], (self.feldgroesse, self.feldgroesse))

    def run(self):
        """Startet die Hauptspiel-Schleife"""
        aktZeit = pygame.time.get_ticks()
        if self.spielfeld.holeZeit()==True:
            if aktZeit - self.letztZeit >= 1000:  # 1000 milliseconds = 1 second
                self.letztZeit = aktZeit
                if self.timer > 0:
                    self.timer -= 1
                else:
                    figur = self.spielfeld.figuren['rot'][0]
                    self.wuerfelw.rolleWuerfel()
                    wuerfel_zahl = self.spielfeld.wuerfel.holeZahl()
                    self.wuerfelw.aktualisiereWuerfelMaske(wuerfel_zahl)  # Update dice display
                    self.reset_timer()

        if self.spielfeld.wuerfel.hatGewuerfelt() == True:
            self.reset_timer()
            self.spielfeld.wuerfel.setzeHatGewuerfelt(False)

        self.zeichneBrett()
        self.zeigeTimer()


    def reset_timer(self):
        """Resets the game timer"""
        self.timer = self.timerStart
        self.letztZeit = pygame.time.get_ticks()


    def zeichneBrett(self):
        """Zeichnet das komplette Spielfeld"""
        self.screen.fill(self.weiss)

        # Spielfeld Position berechnen
        self.brett_start_x = (self.WIDTH - self.groesse * self.feldgroesse) / 2
        self.brett_start_y = (self.HEIGHT - self.groesse * self.feldgroesse) / 2


        # Spielfeld zeichnen
        for reihe in range(self.groesse):
            for spalte in range(self.groesse):
                rect = pygame.Rect(
                    self.brett_start_x + spalte * self.feldgroesse,
                    self.brett_start_y + reihe * self.feldgroesse,
                    self.feldgroesse, self.feldgroesse
                )

                # Laufpfade: Hauptlinien
                if self.angeklicktesFeld == (reihe, spalte):
                    pygame.draw.circle(self.screen, self.hellblau, rect.center, self.kreisradius)
                else:
                    for feld in self.spielfeld._SFeld:
                        if feld.position == (reihe, spalte):
                            pygame.draw.circle(self.screen, self.schwarz, rect.center, self.kreisradius)
                            pygame.draw.circle(self.screen, self.weiss, rect.center, self.kreisradius - 3)

                            
        for farbe, positionen in self.startfeld.items():
            for (reihe, spalte) in positionen:
                center_x = self.brett_start_x + spalte * self.feldgroesse + self.feldgroesse / 2
                center_y = self.brett_start_y + reihe * self.feldgroesse + self.feldgroesse / 2
                if self.angeklicktesFeld == (reihe, spalte):
                    pygame.draw.circle(self.screen, self.hellblau, rect.center, self.kreisradius)
                else:
                    pygame.draw.circle(self.screen, self.uebersetzeFarbe(farbe), (center_x, center_y), self.kreisradius)

        # Start- und Zielfelder zeichnen
        self.zeichneStartUndZiel()
        self.zeichneFiguren()

    def zeigeTimer(self):
        """Zeigt den Countdown-Timer auf dem Bildschirm an"""
        timer_text = self.font.render(f"Zeit übrig: {self.timer}s", True, self.schwarz)
        self.screen.blit(timer_text, (10, 10))

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
        y_offset = -10

        for figurenl in self.spielfeld.figuren.values():
            for figur in figurenl:
                if figur.position:
                    reihe, spalte = figur.holePosition()
                    bild = self.figurenBilder[figur.holeFarbe()]
                    rect = pygame.Rect(
                        self.brett_start_x + spalte * self.feldgroesse,
                        self.brett_start_y + reihe * self.feldgroesse + y_offset,
                        self.feldgroesse, self.feldgroesse
                    )
                    # print(f"Figur {figur.farbe} kreiert")
                    self.screen.blit(bild, rect.topleft)

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
                    # if feld.ist_start:
                    #     print("STARTFELD")
                    #     # print(feld.farbe)
                    # elif feld.ist_ziel:
                    #     print("ZIELFELD")
                    #     # print(feld.farbe)
                    return reihe, spalte
                
            for feld in self.spielfeld.startFeld:
                if feld.holePosition() == (reihe, spalte):
                    # print("STARTFELD")
                    # print(feld.farbe)
                    return reihe, spalte
        
    def Mausklick(self, pos):
        """Handle the mouse click event"""
        feld_pos = self.holeFeld(pos)
        if feld_pos is None:
            self.angeklicktesFeld = None
            return

        for farbe, figuren in self.spielfeld.figuren.items():
            for figur in figuren:
                if figur.holePosition() == feld_pos:
                    self.angeklicktesFeld = feld_pos
                    # print(f"Figure {figur.holeFarbe()} at {self.angeklicktesFeld} clicked")
                    self.spielfeld.setzeNaechsteFigur(figur)
                    print(self.spielfeld.holeNaechsteFigur())
                    return
        
        if self.angeklicktesFeld == feld_pos:
            return
        else:
            # if feld_pos == figur
            if feld_pos:
                self.angeklicktesFeld = feld_pos
                print(f"Feld {self.angeklicktesFeld}")
            else:
                self.angeklicktesFeld = None


    def uebersetzeFarbe(self, farbe):
        """gibt die Farbe als globale Variable zurück"""
        farben = {
            'rot': self.rot,
            'blau': self.blau,
            'gelb': self.gelb,
            'gruen': self.gruen,
        }
        return farben.get(farbe, self.schwarz)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    spielfeld_gui = PygameWidget()
    spielfeld_gui.show()
    sys.exit(app.exec_())