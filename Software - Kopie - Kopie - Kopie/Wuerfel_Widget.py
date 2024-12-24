import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class WuerfelWidget(QWidget):
    def __init__(self, spielfeld):
        super().__init__()
        self.initUI()
        self.spielfeld = spielfeld

        self.status_timer = QTimer()
        self.status_timer.setSingleShot(False)
        self.status_timer.timeout.connect(self.updateWuerfelAktiv)
        self.status_timer.start(100)  # Überprüft alle 100 ms
        
    def initUI(self):
        self.setWindowTitle('Wuerfel')
        self.setGeometry(100, 100, 300, 300)
        
        # Layout
        layout = QVBoxLayout()
        
        # Roll buttons
        self.wuerfelButton = QPushButton('Rolle Wuerfel', self)
        self.wuerfelButton.clicked.connect(self.rolleWuerfel)
        layout.addWidget(self.wuerfelButton)
    
        
        # Dice wert labels
        self.wuerfelLabel = QLabel('Würfel!', self)
        self.wuerfelLabel.setAlignment(Qt.AlignBottom)
        self.wuerfelLabel.setFont(QFont('Arial', 24))
        layout.addWidget(self.wuerfelLabel)
               
        self.setLayout(layout)
    

    def rolleWuerfel(self):
        self.spielfeld.wuerfel.rollen()  # Roll the dice
        wuerfel_zahl = self.spielfeld.wuerfel.holeZahl()  # Get the rolled wert
        self.aktualisiereWuerfelMaske(wuerfel_zahl)

        naechsteFigur = self.spielfeld.figuren['rot'][0]
        
        if naechsteFigur is None:
            verfuegbare_figuren = self.spielfeld.verfuegbareFiguren("rot")
            print(verfuegbare_figuren)
            if len(verfuegbare_figuren) == 1:
                # Automatisch die einzige verfügbare Figur bewegen
                self.spielfeld.bewegeFigur(verfuegbare_figuren[0], wuerfel_zahl)
            elif len(verfuegbare_figuren) > 1:
                # Benutzer muss eine Figur auswählen
                print("Bitte wählen Sie eine Figur aus.")
                self.spielfeld.setzeNaechsteFigur(None)
                self.spielfeld.warte()
            else:
                print("KEINE FIGUR VERFÜGBAR")
        else:
            self.spielfeld.bewegeFigur(naechsteFigur, wuerfel_zahl)
            self.spielfeld.setzeNaechsteFigur(None)  # Reset nach der Bewegung

        self.spielfeld.wuerfel.setzeHatGewuerfelt(True)
        self.updateWuerfelAktiv()

    def updateWuerfelAktiv(self):
        if self.spielfeld.holeAktiv() != True:
            self.wuerfelButton.setDisabled(True)
        else:
            self.wuerfelButton.setDisabled(False)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        # Draw positive dice
        if self.spielfeld.wuerfel.holeZahl() is not None:
            self.zeichneWuerfel(painter, 60, 60, self.spielfeld.wuerfel.holeZahl())
    
    def zeichneWuerfel(self, painter, x, y, wert):
        d = 180
        painter.setBrush(QColor(255, 255, 255))
        painter.drawRect(x, y, d, d)
        painter.setPen(QColor(0, 0, 0))
        
        # Draw dots based on the dice wert
        punkt_position = {
            1: [(80, 80)],
            2: [(40, 40), (120, 120)],
            3: [(40, 40), (80, 80), (120, 120)],
            4: [(40, 40), (40, 120), (120, 40), (120, 120)],
            5: [(40, 40), (40, 120), (80, 80), (120, 40), (120, 120)],
            6: [(40, 40), (40, 80), (40, 120), (120, 40), (120, 80), (120, 120)],
        }
        if wert == 0:
            return
        else:
            for pos in punkt_position[wert]:
                painter.drawEllipse(x + int(pos[0]), y + int(pos[1]), 20, 20)

    def aktualisiereWuerfelMaske(self, wuerfel_zahl):
        """Updates the dice display with the given wert"""
        self.wuerfelLabel.setText(f'Positiver Wuerfel: {wuerfel_zahl}')
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wuerfelWidget = WuerfelWidget()
    wuerfelWidget.show()
    sys.exit(app.exec_())