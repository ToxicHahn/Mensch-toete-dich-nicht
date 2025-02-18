import sys
from random import randint
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel
import webcolors
import socket
import threading
import time


# GUI
class MenschAergereDichNicht(QWidget):
    def __init__(self, c1, c2, c3, c4, player, client_socket, client_ins):
        super().__init__()
        self.client_ins = client_ins
        self.figurenNames = {}
        self.already = 0
        #self.spiel_logik = SpielLogik([c1, c2, c3, c4])
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.c4 = c4
        self.c = [self.c1, self.c2, self.c3, self.c4]
        self.game = []

        self.state = 0

        self.wuerfel_ergebnis = None

        self.player = player
        #print(f'MÄDN {self.player}')


        self.feld_nach_c1 = {
            (0, 0): (4, 0),(0, 1): (4, 0),(1, 0): (4, 0),(1, 1): (4, 0),(4, 0): (4, 1),(4, 1): (4, 2),(4, 2): (4, 3),(4, 3): (4, 4),(4, 4): (3, 4),
            (3, 4): (2, 4),(2, 4): (1, 4),(1, 4): (0, 4),(0, 4): (0, 5),(0, 5): (0, 6),(0, 6): (1, 6),(1, 6): (2, 6),(2, 6): (3, 6),(3, 6): (4, 6),
            (4, 6): (4, 7),(4, 7): (4, 8),(4, 8): (4, 9),(4, 9): (4, 10),(4, 10): (5, 10),(5, 10): (6, 10),(6, 10): (6, 9),(6, 9): (6, 8),(6, 8): (6, 7),
            (6, 7): (6, 6),(6, 6): (7, 6),(7, 6): (8, 6),(8, 6): (9, 6),(9, 6): (10, 6),(10, 6): (10, 5),(10, 5): (10, 4),(10, 4): (9, 4),(9, 4): (8, 4),
            (8, 4): (7, 4),(7, 4): (6, 4),(6, 4): (6, 3),(6, 3): (6, 2),(6, 2): (6, 1),(6, 1): (6, 0),(6, 0): (5, 0),
            (5, 0): (5, 1),(5, 1): (5, 2),(5, 2): (5, 3),(5, 3): (5, 4),
        }
        self.feld_nach_c2 = {
            (0, 9): (0, 6),(0, 10): (0, 6),(1, 9): (0, 6),(1, 10): (0, 6),

            (0, 6): (1, 6),(1, 6): (2, 6),(2, 6): (3, 6),(3, 6): (4, 6),
            (4, 6): (4, 7),(4, 7): (4, 8),(4, 8): (4, 9),(4, 9): (4, 10),(4, 10): (5, 10),(5, 10): (6, 10),(6, 10): (6, 9),(6, 9): (6, 8),(6, 8): (6, 7),
            (6, 7): (6, 6),(6, 6): (7, 6),(7, 6): (8, 6),(8, 6): (9, 6),(9, 6): (10, 6),(10, 6): (10, 5),(10, 5): (10, 4),(10, 4): (9, 4),(9, 4): (8, 4),
            (8, 4): (7, 4),(7, 4): (6, 4),(6, 4): (6, 3),(6, 3): (6, 2),(6, 2): (6, 1),(6, 1): (6, 0),(6, 0): (5, 0), (5,0): (4,0),

            (4, 0): (4, 1),(4, 1): (4, 2),(4, 2): (4, 3),(4, 3): (4, 4),(4, 4): (3, 4),
            (3, 4): (2, 4),(2, 4): (1, 4),(1, 4): (0, 4),(0, 4): (0, 5),

            (0, 5): (1, 5),(1, 5): (2, 5),(2, 5): (3, 5),(3, 5): (4, 5),
        }
        self.feld_nach_c3 = {
            (9, 9): (6, 10),(9, 10): (6, 10),(10, 9): (6, 10),(10, 10): (6, 10),

            (6, 10): (6, 9),(6, 9): (6, 8),(6, 8): (6, 7),
            (6, 7): (6, 6),(6, 6): (7, 6),(7, 6): (8, 6),(8, 6): (9, 6),(9, 6): (10, 6),(10, 6): (10, 5),(10, 5): (10, 4),(10, 4): (9, 4),(9, 4): (8, 4),
            (8, 4): (7, 4),(7, 4): (6, 4),(6, 4): (6, 3),(6, 3): (6, 2),(6, 2): (6, 1),(6, 1): (6, 0),(6, 0): (5, 0), (5,0): (4,0),

            (4, 0): (4, 1),(4, 1): (4, 2),(4, 2): (4, 3),(4, 3): (4, 4),(4, 4): (3, 4),
            (3, 4): (2, 4),(2, 4): (1, 4),(1, 4): (0, 4),(0, 4): (0, 5),(0, 5): (0, 6),
            
            (0, 6): (1, 6),(1, 6): (2, 6),(2, 6): (3, 6),(3, 6): (4, 6),
            (4, 6): (4, 7),(4, 7): (4, 8),(4, 8): (4, 9),(4, 9): (4, 10),(4, 10): (5, 10),(5, 10): (5, 9),

            (5, 10): (5, 9),(5, 9): (5, 8),(5, 8): (5, 7),(5, 7): (5, 6),
        }
        self.feld_nach_c4 = {
            (9, 0): (10, 4),(9, 1): (10, 4),(10, 0): (10, 4),(10, 1): (10, 4),

            (10, 4): (9, 4),(9, 4): (8, 4),(8, 4): (7, 4),(7, 4): (6, 4),(6, 4): (6, 3),(6, 3): (6, 2),(6, 2): (6, 1),(6, 1): (6, 0),(6, 0): (5, 0), (5,0): (4,0),

            (4, 0): (4, 1),(4, 1): (4, 2),(4, 2): (4, 3),(4, 3): (4, 4),(4, 4): (3, 4),
            (3, 4): (2, 4),(2, 4): (1, 4),(1, 4): (0, 4),(0, 4): (0, 5),(0, 5): (0, 6),
            
            (0, 6): (1, 6),(1, 6): (2, 6),(2, 6): (3, 6),(3, 6): (4, 6),
            (4, 6): (4, 7),(4, 7): (4, 8),(4, 8): (4, 9),(4, 9): (4, 10),(4, 10): (5, 10),(5, 10): (6, 10),

            (6, 10): (6, 9),(6, 9): (6, 8),(6, 8): (6, 7),
            (6, 7): (6, 6),(6, 6): (7, 6),(7, 6): (8, 6),(8, 6): (9, 6),(9, 6): (10, 6),(10, 6): (10, 5),
            
            (10, 5): (9, 5),(9, 5): (8, 5),(8, 5): (7, 5),(7, 5): (6, 5),
        }



        self.setWindowTitle("Mensch ärgere Dich nicht")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #2d2d2d;")

        self.setFixedSize(500, 600)

        self.grid_layout = QGridLayout()
        self.buttons = {}
        self.figuren = {}
        self.figurenc1 = []
        self.figurenc2 = []
        self.figurenc3 = []
        self.figurenc4 = []


        self.selected_button = None

        self.create_cross_board()
        self.create_figuren()

        self.status_label = QLabel("Warte auf Server...")
        self.status_label.setStyleSheet("color: white; font-size: 16px;")
        self.dice_label = QLabel("Würfel: -")
        self.dice_label.setStyleSheet("color: white; font-size: 16px;")

        # Würfeln-Button
        self.roll_button = QPushButton("End Move")
        self.roll_button.setStyleSheet(f"background-color: {self.player}; font-size: 16px; padding: 10px;")
        self.roll_button.clicked.connect(lambda: self.endMove(2))
        self.roll_button.setEnabled(False)

        # Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.dice_label)
        main_layout.addLayout(self.grid_layout)
        main_layout.addWidget(self.roll_button)
        self.setLayout(main_layout)
        self.client_socket = client_socket

        self.startc1 = [(0,0),(0,1),(1,0),(1,1)]
        self.startc2 = [(0,9),(0,10),(1,9),(1,10)]
        self.startc3 = [(9,9),(9,10),(10,9),(10,10)]
        self.startc4 = [(9,0),(9,1),(10,0),(10,1)]

    def setState(self, x):
        self.state = x


    def create_cross_board(self):
        positions = [
            (0,4), (0,5), (0,6), (1,4), (1,6),
            (2,4), (2,6), (3,4), (3,6), (4,0),
            (4,1), (4,2), (4,3), (4,4), 
            (4,6), (4,7), (4,8), (4,9),
            (4,10), (5,0), (5,10), (6,0),
            (6,1), (6,2), (6,3), (6,4),
            (6,6), (6,7), (6,8), (6,9), (6,10),
            (7,4), (7,6), (8,4), (8,6),
            (9,4), (9,6), (10,4), (10,5), (10,6),

            (0,0),(1,0),(0,1),(1,1),
            (0,9),(1,9),(0,10),(1,10),
            (9,9),(9,10),(10,9),(10,10),
            (9,0),(9,1),(10,0),(10,1),


            
            (5,1),(5,2),(5,3),(5,4),
            (1,5),(2,5),(3,5),(4,5),
            (6,5),(7,5),(8,5),(9,5),
            (5,6),(5,7),(5,8),(5,9),

        ]
        
        for row in range(11):
            for col in range(11):
                button = QPushButton()
                button.setFixedSize(40, 40)
                
                if (row, col) in positions:
                    if (row, col) in [(0,0),(1,0),(0,1),(1,1),(5,1),(5,2),(5,3),(5,4),(4,0),]:
                        button.setStyleSheet(f'background-color: {self.c1}; border: 2px solid black;')
                        button.setText(f'{row}/{col}')
                    elif (row, col) in [(0,9),(1,9),(0,10),(1,10),(1,5),(2,5),(3,5),(4,5),(0,6),]:
                        button.setStyleSheet(f'background-color: {self.c2}; border: 2px solid black;')
                        button.setText(f'{row}/{col}')
                    elif (row, col) in [(9,9),(9,10),(10,9),(10,10),(5,6),(5,7),(5,8),(5,9),(6,10),]:
                        button.setStyleSheet(f'background-color: {self.c3}; border: 2px solid black;')
                        button.setText(f'{row}/{col}')
                    elif (row, col) in [(9,0),(9,1),(10,0),(10,1),(6,5),(7,5),(8,5),(9,5),(10,4),]:
                        button.setStyleSheet(f'background-color: {self.c4}; border: 2px solid black;')
                        button.setText(f'{row}/{col}')
                    
                    
                    else:
                        button.setStyleSheet("background-color: lightblue; border: 1px solid black;")
                        #button.setText(f'{row}/{col}')
                    
                    button.clicked.connect(self.on_field_clicked)
                    self.buttons[(row, col)] = button
                    self.grid_layout.addWidget(button, row, col)

    def create_figuren(self):
        # Definiertt Ecken
        startfelder = [
            (0,0), (1,0), (0,1), (1,1),
            (0,9), (1,9), (0,10), (1,10),
            (9,0), (9,1), (10,0), (10,1),
            (9,9), (9,10), (10,9), (10,10),
        ]

        # Erstelle dasds Spielfeld
        for row in range(11):
            for col in range(11):
                if (row,col) in startfelder:
                    x = f'button{row,col}'
                    button = QPushButton()
                    button.setFixedSize(40, 40)
                    button.setObjectName(x)

                    #if (row, col) in startfelder:
                        # Setzt die runden Buttons nur auf die Ecken (Startfelder)
                    button.setStyleSheet('border-radius: 20px;')  # Macht die Buttons rund

                    if (row, col) in [(0,0), (1,0), (0,1), (1,1)]:
                        button.setStyleSheet(f'background-color: {self.c1}; border: 2px solid black; border-radius: 20px;')
                        if (row, col) == (0,0):
                            button.setText("1")
                        elif (row, col) == (0,1):
                            button.setText("2")
                        elif (row, col) == (1,0):
                            button.setText("3")
                        elif (row, col) == (1,1):
                            button.setText("4")
                    elif (row, col) in [(0,9), (1,9), (0,10), (1,10)]:
                        button.setStyleSheet(f'background-color: {self.c2}; border: 2px solid black; border-radius: 20px;')
                        if (row, col) == (0,9):
                            button.setText("1")
                        elif (row, col) == (0,10):
                            button.setText("2")
                        elif (row, col) == (1,9):
                            button.setText("3")
                        elif (row, col) == (1,10):
                            button.setText("4")                    
                    elif (row, col) in [(9,9), (9,10), (10,9), (10,10)]:
                        button.setStyleSheet(f'background-color: {self.c3}; border: 2px solid black; border-radius: 20px;')
                        if (row, col) == (9,9):
                            button.setText("1")
                        elif (row, col) == (9,10):
                            button.setText("2")
                        elif (row, col) == (10,9):
                            button.setText("3")
                        elif (row, col) == (10,10):
                            button.setText("4")
                    elif (row, col) in [(9,0), (9,1), (10,0), (10,1)]:
                        button.setStyleSheet(f'background-color: {self.c4}; border: 2px solid black; border-radius: 20px;')
                        if (row, col) == (9,0):
                            button.setText("1")
                        elif (row, col) == (9,1):
                            button.setText("2")
                        elif (row, col) == (10,0):
                            button.setText("3")
                        elif (row, col) == (10,1):
                            button.setText("4")
                    if  self.get_background_color(button)== self.c1:
                        f = (row, col)
                        self.figurenc1.append(f)
                    elif self.get_background_color(button)== self.c2:
                        f = (row, col)
                        self.figurenc2.append(f)
                    elif self.get_background_color(button)== self.c3:
                        f = (row, col)
                        self.figurenc3.append(f)
                    elif self.get_background_color(button)== self.c4:
                        f = (row, col)
                        self.figurenc4.append(f)


                    # funktion button click
                    button.clicked.connect(self.on_figur_clicked)
                    self.figuren[(row, col)] = button
                    self.figurenNames[button.objectName()] = button
                    self.grid_layout.addWidget(button, row, col)

    def get_background_color(self, button):

        stylesheet = button.styleSheet()
        
        # Prüfe, ob das Stylesheet eine Hintergrundfarbe angibt
        if 'background-color' in stylesheet:
            # bgc aus ss holen
            start = stylesheet.find('background-color:') + len('background-color:')
            end = stylesheet.find(';', start)
            background_color = stylesheet[start:end].strip()
            return background_color
        return None

    def on_field_clicked(self):
        if self.state == 1:
            button = self.sender()
            
            current_color = button.palette().button().color().name()
            if current_color != "#add8e6":
                #self.status_label.setText("keijene auswah!")
                return
            
            if self.selected_button:
                self.selected_button.setStyleSheet("background-color: lightblue; border: 1px solid black;")
            button.setStyleSheet("background-color: orange; border: 1px solid black;")
            self.selected_button = button
            #self.status_label.setText(f"Feld {button} ausgewählt")

    def on_figur_clicked(self):
        #print("OK")
        if self.state == 1:
            buttonf = self.sender().objectName()
            buttong = self.sender()
            
            colorf = buttong.palette().button().color().name()
            current_colorf = webcolors.hex_to_name(colorf)

            if current_colorf != self.player:
                #print("COLOR")
                return
            if self.wuerfel_ergebnis:
                ausgang = self.get_button_coordinates(buttong)
                #print(ausgang)
                #print(self.wuerfel_ergebnis)
                #print(type(buttonf))
                self.client_socket.send(f'/move#{self.player}#{ausgang}#{buttonf}#{self.wuerfel_ergebnis}'.encode())
                time.sleep(0.1)
                ausgang = str(ausgang)
                #print(ausgang)
                self.move(self.player, buttonf, ausgang, self.wuerfel_ergebnis, 1)
            self.wuerfel_ergebnis = None
            self.status_label.setText("Warte... Ein Gegner ist dran.")
            self.state = 0

    def roll_dice(self):
        self.wuerfel_ergebnis = randint(6,6)
        self.dice_label.setText(f"Würfel: {self.wuerfel_ergebnis}")
        self.roll_button.setEnabled(False)
        # swittch nächster spielr
        self.state = 1
        #self.spiel_logik.naechster_spieler()
        #self.update()

    def get_button_coordinates(self, button):
        # Index button
        index = self.grid_layout.indexOf(button)
        
        # zeile/spaalte
        row = self.grid_layout.getItemPosition(index)[0]
        col = self.grid_layout.getItemPosition(index)[1]
        
        return row, col
        

    def move(self, player, button, ausgang, fields, index):
        #fields = self.wuerfel_ergebnis
        nächstes_feld = ()
        #print(f'{self.player}, {index}')
        ausgang = eval(ausgang)
        #print(ausgang)

        if ausgang in [(0, 0),(1, 0),(0, 1),(1, 1),(0, 9),(1, 9),(0, 10),(1, 10),(9, 0),(9, 1),(10, 0),(10, 1),(9, 9),(9, 10),(10, 9),(10, 10)]:
            #print("JA")
            ausgangI = ausgang
            if fields == 6:
                #print(player)
                if player == self.c1:
                    #print("EIGENTLICXH")
                    nächstes_feld = self.feld_nach_c1.get(ausgang, [])
                    #print("NF")
                elif player == self.c2:
                    nächstes_feld = self.feld_nach_c2.get(ausgang, [])
                    #print("NF")
                elif player == self.c3:
                    nächstes_feld = self.feld_nach_c3.get(ausgang, [])
                    #print("NF")
                elif player == self.c4:
                    nächstes_feld = self.feld_nach_c4.get(ausgang, [])
                    #print("NF")

                if not nächstes_feld:
                    #print("NOT NÄCHSTES FELD")
                    self.endMove(index)
                    return
                else:
                    print(f'KOLLISION: {self.kollidiert(nächstes_feld)}')
                    if self.kollidiert(nächstes_feld) == True:
                        self.kollision(button, nächstes_feld, ausgangI, index, player)
                        return                        
                    #print("button")
                    #print(index)
                    #if index == 0:
                    #    button = button.objectName()
                    #print(f'BUTTON {button}')
                    widget = self.findChild(QPushButton, button)
                    #print(f'WIDGET {widget}')
                    #print(ausgang)
                    self.move_button(widget, nächstes_feld[0], nächstes_feld[1], ausgang, index, player, nächstes_feld)
                    return
            else:
                self.endMove(2)
                return
        else:
            # Normale Bewegung
            print("NORMALE BEWEGUNG #####################")
            ausgangI = ausgang
            for i in range(fields):
                if i != 0:
                    ausgang = nächstes_feld

                if player == self.c1:
                    nächstes_feld = self.feld_nach_c1.get(ausgang, ())
                elif player == self.c2:
                    nächstes_feld = self.feld_nach_c2.get(ausgang, ())
                elif player == self.c3:
                    nächstes_feld = self.feld_nach_c3.get(ausgang, ())
                elif player == self.c4:
                    nächstes_feld = self.feld_nach_c4.get(ausgang, ())

                #print(f"Zwischenschritt {i}: Ausgang={ausgang}, nächstes Feld={nächstes_feld}")



            if not nächstes_feld:
                #print(f"Bewegung abgebrochen: Kein nächstes Feld für {ausgang}.")
                self.endMove(2)
                return
            else:
                print("Kollision ?")
                if self.kollidiert(nächstes_feld) == True:
                    self.kollision(button, nächstes_feld, ausgangI, index, player)
                    return
        
            #if index == 1:
            #        button = button.objectName()
            widget = self.findChild(QPushButton, button)
            #print(f'WIDGET {widget}')
            self.move_button(widget, nächstes_feld[0], nächstes_feld[1], ausgangI, index, player, nächstes_feld)
            return
            


                # Letzter Schritt
                #try:
                #    alt = self.figuren[nächstes_feld]
                #    print(f'ALT {alt}')
                #    altt = self.findChild(QPushButton, alt)
                #    print(f'ALTT {altt}')
                        #    self.move_button(altt, nächstes_feld[0], nächstes_feld[1], ausgang, index)
                #except Exception as e:
                            #    print(f"Fehler beim Bewegen des Buttons: {e}")
                #    if index == 1:
                #        self.endMove(1)
                #    else:
                    #        self.endMove(0)
            #ex     cept Exception as e:
            #   print(f"Allgemeiner Fehler in move: {e}")


    def updateListC1(self, index, wert):
        if 0 <= index < len(self.figurenc1):
            self.figurenc1[index] = wert
        else:
            print(f"Ungültiger Index: {index}")

    def updateListC2(self, index, wert):
        if 0 <= index < len(self.figurenc2):
            self.figurenc2[index] = wert
        else:
            print(f"Ungültiger Index: {index}")

    def updateListC3(self, index, wert):
        if 0 <= index < len(self.figurenc3):
            self.figurenc3[index] = wert
        else:
            print(f"Ungültiger Index: {index}")

    def updateListC4(self, index, wert):
        if 0 <= index < len(self.figurenc4):
            self.figurenc4[index] = wert
        else:
            print(f"Ungültiger Index: {index}")

    def kollision(self, button, nächstes_feld, ausgang, index, player):
        print("Kollision")
        kick_player = self.figuren[nächstes_feld]
        self.figuren[ausgang] = button
        print(kick_player)
        kick_player_player = self.get_background_color(kick_player)
        if kick_player_player in self.game:
            self.endMove(2)
            return
        
        innF = int(kick_player.text())
        inn = innF -1
        if kick_player_player == self.c1:
            neues_feld = self.startc1[inn]
        elif kick_player_player == self.c2:
            neues_feld = self.startc2[inn]
        elif kick_player_player == self.c3:
            neues_feld = self.startc3[inn]
        elif kick_player_player == self.c4:
            neues_feld = self.startc4[inn]

        
        print(f'KICK PLAYER {kick_player}')
        print(f'BUTTON {button}')

        new_row = nächstes_feld[0]
        new_col = nächstes_feld[1]
        #self.figurenNames[button] = buttons
        widget = self.findChild(QPushButton, button)
        self.move_button(widget, new_row, new_col, ausgang, index, player, nächstes_feld)
        self.move_button(kick_player, neues_feld[0], neues_feld[1], nächstes_feld, 0, kick_player_player, neues_feld)
        return
    
    def kollidiert(self, nächstes_feld):
        if nächstes_feld in self.figuren:
            return True
        else:
           return False
        




    def alle_Haus(self):
        if self.c1 == self.player:
            home = [(0,0), (0,1), (1,0), (1,1)]
        elif self.c2 == self.player:
            home = [(0,9),(0,10),(1,9),(1,10)]
        elif self.c3 == self.player:
            home = [(9,9),(9,10),(10,9),(10,10)]
        elif self.c4 == self.player:
            home = [(9,0),(9,1),(10,0),(10,1)]
        #print(self.figurenc1)
        #print(home)
        if self.player == self.c1: 
            f = self.figurenc1
        elif self.player == self.c2:
            f = self.figurenc2
        elif self.player == self.c3:
            f = self.figurenc3
        elif self.player == self.c4:
            f = self.figurenc4
        for i in range(len(home)):
            if not home[i] == f[i]:
                    return False
        return True
    
    def gewonnen(self, player):
        if self.c1 == player:
            home = [(5,1),(5,2),(5,3),(5,4)]
            f = self.figurenc1
        elif self.c2 == player:
            home = [(1,5),(2,5),(3,5),(4,5)]
            f = self.figurenc2
        elif self.c3 == player:
            home = [(5,6),(5,7),(5,8),(5,9)]
            f = self.figurenc3
        elif self.c4 == player:
            home = [(6,5),(7,5),(8,5),(9,5)]
            f = self.figurenc4
        #print(self.figurenc1)
        #print(home)
        print(f'Gewonnen?: {self.elements_in_list(home, f)}')
        return self.elements_in_list(home, f)
    
    def elements_in_list(self, elements, lst):
        print(elements, lst)
        return set(elements).issubset(lst)



    def move_button(self, button, new_row, new_col, ausgang, indexx, player, nächstes_Feld):
        #print(f'AUSGANG {ausgang}')
        if isinstance(button, QWidget):  # Überprüfe, ob es sich um einen Button handelt
            # Entferne den Button aus der aktuellen Position im Layout
            self.grid_layout.removeWidget(button)
            button.setParent(None)  # Entferne den Button von der alten Eltern (optional)

            self.grid_layout.addWidget(button, new_row, new_col)


            x = new_row, new_col
            if player == self.c1:
                #print("INDEX USW")
                index = self.figurenc1.index(ausgang)
                self.figurenc1[index] = x
            elif player == self.c2:
                index = self.figurenc2.index(ausgang)
                self.figurenc2[index] = x
            elif player == self.c3:
                index = self.figurenc3.index(ausgang)
                self.figurenc3[index] = x
            elif player == self.c4:
                index = self.figurenc4.index(ausgang)
                self.figurenc4[index] = x


            key_to_update = ausgang


            
            if key_to_update in self.figuren:
                # lösche alten ke<y
                old_value = self.figuren.pop(key_to_update)
                
                # Füge den neuen Schlüssel mit allterm wert hin
                self.figuren[x] = old_value

            if self.player == player:
                if self.gewonnen(player) == True:
                    self.client_socket.send(f'/win {player}'.encode())
                    time.sleep(0.1)
                    return
            self.figuren[(new_row, new_col)] = button
            button.show()
            self.endMove(indexx)
            return
                
        else:
            print("Fehler: Das übergebene Argument ist kein Widget.")
        #print(self.figurenc1)
        #print(self.figurenc2)
        #print(self.figurenc3)
        #print(self.figurenc4)
        if indexx == 1:
            self.client_socket.send(f'/done {self.player}'.encode())
            time.sleep(0.1)
            self.already = 1
        return


    def getName(self):
        return self.player

    def endMove(self, index):
        from yy import Client as Client
        self.state = 0
        self.roll_button.setEnabled(False)
        self.status_label.setText("Warte auf Server...")
        #print("END FELD")
        Client.endMove(self, index)
        #print("ENDE END MOVE")
        #print(f'FIGUREN C1: {self.figurenc1}')



    def turn(self, wuerfel, client_socket):
        self.already = 0
        #print("1")
        #print(self.alle_Haus())
        self.wuerfel_ergebnis = wuerfel
        self.roll_button.setEnabled(True)
        self.dice_label.setText(f"Würfel: {wuerfel}")
        if self.alle_Haus() == True and not wuerfel == 6:
            #print("END MOVE")
            self.endMove(1)
            return
        self.client_socket = client_socket
        self.state = 1
        self.status_label.setText("Sie sind dran!")
        