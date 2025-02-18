import sys
import socket
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QLineEdit, QGraphicsDropShadowEffect
from PyQt5.QtCore import QThread, pyqtSignal
from random import randint
from SPIELFELDD import MenschAergereDichNicht
import time
#from join_gui import JoinGui

class ClientThread(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, client_socket, parent=None, client_ins=None):
        super().__init__(parent)
        self.client_socket = client_socket
        self.client_ins = client_ins

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    self.message_received.emit(message)  # Signal an Hauptthread senden
            except Exception as e:
                print(f"Fehler beim Empfangen der Nachricht: {e}")
                break


class Client(QWidget):
    def __init__(self, player, host = '10.16.206.7', port=5000):
        super().__init__()
        self.playerr = None
        self.player = player
        print(self.player)
        self.host = host
        self.port = port
        #self.client_socket = None
        self.dice_result = 0

        self.c1 = ""
        self.c2 = ""
        self.c3 = ""
        self.c4 = ""

        #self.hostt = input("Host: ")
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect_to_server()
        self.client_socket.send(f"/color#{self.player}".encode())
 
    def create_board(self):
        self.layout = QVBoxLayout()
        self.m = MenschAergereDichNicht(self.c1, self.c2, self.c3, self.c4, self.player, self.client_socket, self)
        self.layout.addWidget(self.m)
        self.setWindowTitle('Mensch ärgere Dich nicht')

        self.roll_button = QPushButton('Würfeln', self)
        self.roll_button.clicked.connect(self.roll_dice)
        self.layout.addWidget(self.roll_button)
        self.roll_button.setEnabled(False)
        self.quit_button = QPushButton('Beenden', self)
        self.quit_button.clicked.connect(self.quit_game)
        self.layout.addWidget(self.quit_button)
        self.status_label = QLabel("Warte auf Server...")
        self.layout.addWidget(self.status_label)

        # Textfeld für die Anzeige von Nachrichten
        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        # Eingabefeld für den Benutzernamen
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Gib deinen Benutzernamen ein")
        self.layout.addWidget(self.username_input)

        # Eingabefeld für die Nachricht
        self.input_field = QLineEdit(self)
        self.layout.addWidget(self.input_field)

        # Eingabefeld für den Ziel-Clientnamen (für Flüster-Nachricht)
        self.target_field = QLineEdit(self)
        self.target_field.setPlaceholderText("Flüster an (Benutzernamen):")
        self.layout.addWidget(self.target_field)

        # Senden-Button
        self.send_button = QPushButton("Senden", self)
        self.layout.addWidget(self.send_button)

        # Verbinden des Buttons mit der Funktion
        self.send_button.clicked.connect(self.send_message)


        self.setLayout(self.layout)
        self.resize(300, 200)
        self.show()


    def send_message(self):

        message = self.input_field.text()

        target_client = self.target_field.text()

        if message:
            if target_client:  # Flüster-Nachricht, wenn ein Zielname angegeben wurde
                whisper_message = f"/whisper#{message}#{self.player}#{target_client}"
                self.client_socket.send(whisper_message.encode('utf-8'))  # Flüster-Nachricht senden
                self.text_display.append(f"Du flüsterst an {target_client}: {message}")
            else:  # Normale Nachricht senden
                try:
                    broadcast_message = f"/message#{message}#{self.player}"
                    self.client_socket.send(broadcast_message.encode('utf-8'))
                    self.text_display.append(f"Du: {message}")
                except Exception as e:
                    print(f"Fehler beim Senden der Nachricht: {e}")
                    self.client_socket.close()

            # Eingabefelder leeren
            self.input_field.clear()
            self.target_field.clear()

    def usecolor(self, message):
        if message.startswith("/GAME"):
            self.client_socket.send(message.encode('utf-8'))
        print("USECOLOR")
        parts = message.split("#")
        color1 = parts[1]
        color2 = parts[2]
        color3 = parts[3]
        color4 = parts[4]
        self.c1 = color1
        self.c2 = color2
        self.c3 = color3
        self.c4 = color4
       
    def game(message):
        parts = message.split("#")
        self.m.game.append(parts[1])

    def win(self, message):
        parts = message.split(' ', 2)
        self.status_label.setText(f'Spieler {parts[1]} hat gewonnen!')
        

    def moveF(self, message, client_socket):
        #print(f"Empfangene /move-Nachricht: {message}")
        parts = message.split('#')
        if len(parts) != 5:
            print(f"Ungültige Nachricht: {message}")
            return

        try:
            #print(f"Spieler: {parts[1]}, Button: {parts[3]}, Ausgang: {parts[2]}")
            #print(f'FIELDS {parts[4]}')
            x = int(parts[4])
            #print(x)
            self.m.move(parts[1], parts[3], parts[2], x, 0)
        except Exception as e:
            print(f"Fehler in moveF: {e}")



    def connect_to_server(self):
        try:
            self.client_socket.connect((self.host, self.port))
            self.receive_thread = ClientThread(self.client_socket, client_ins=self)
            self.receive_thread.message_received.connect(self.handle_server_message)  # Signal verbinden
            self.receive_thread.start()
        except Exception as e:
            print("Fehler bei der Verbindung zum Server:", e)

    def handle_server_message(self, message):
        if message.startswith("/turn"):
            self.activate()
            time.sleep(0.1)
        elif message.startswith("/win"):
            self.win(message)
            time.sleep(0.1)
        elif message.startswith("/move"):
            self.moveF(message, self.client_socket)
            time.sleep(0.1)
        elif message.startswith("/player"):
            self.playerB(message)
            time.sleep(0.1)
        elif message.startswith("/finalColor"):
            print("AUFRUF USECOLOR")
            self.usecolor(message)
            time.sleep(0.1)
        elif message.startswith("/start"):
            self.create_board()
            time.sleep(0.1)
        elif message.startswith("/decline"):
            self.declined(message)
            time.sleep(0.1)
        elif message.startswith("/message"):
            self.display_message(message)
        elif message.startswith("/whisper"):
            self.receive_whisper(message)
            time.sleep(0.1)
        elif message.startswith("/GAME"):
            self.game(message)

    def display_message(self, message):
        parts = message.split("#")
        self.text_display.append(f"{parts[2]}: {parts[1]}")

    def receive_whisper(self, message):
        parts = message.split("#")
        messageN = f"{parts[3]} flüstert an Dich: {parts[1]}"
        self.text_display.append(f"Server: {messageN}")

    def declined(self, message):
        from join_gui import JoinGui
        JoinGui.show_error_message(self, message)


    def update_message(self, message):
        print(message)

    def activate(self):
        #print("Enable")
        self.roll_button.setEnabled(True)
        self.m.status_label.setText("Sie sind dran!")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(self.player)
        shadow.setOffset(5, 5)
        self.m.setGraphicsEffect(shadow)
        

    def roll_dice(self):
        self.dice_result = randint(1, 6)
        self.roll_button.setEnabled(False)
        self.m.turn(self.dice_result, self.client_socket)

    def quit_game(self):
        self.client_socket.send('/exit'.encode())
        self.client_socket.close()
        self.close()

    def getPlayer(self):
        return self.player
    
    def endMove(self, index):
        #print(f'{self.player} {index}')
        if index ==2:
            self.client_socket.send(f'/done {self.player}'.encode())
            time.sleep(0.1)
            self.roll_button.setEnabled(False)
            self.dice_result = None
            return
        #if index == 1:
        #    self.client_socket.send(f'/player'.encode())
            #print(self.player)
        #if self.client_ins.playerr:
            #print(f'Playerr {self.client_ins.playerr[0]}')
        elif index == 1 and not self.already == 1:
            self.client_socket.send(f'/done {self.player}'.encode())
            time.sleep(0.1)
        elif self.client_ins.playerr:
            if self.player == self.client_ins.playerr[0]:
                #print(f'{self.player} sendet done')
                self.client_socket.send(f'/done {self.player}'.encode())
                time.sleep(0.1)
        
        self.roll_button.setEnabled(False)
        self.dice_result = None
    
    def playerA(self, message):
        return self.playerr

    def playerB(self, message):
        data = message.split("#")
        self.playerr = data[1]
        #print(f'PlayerB {self.playerr}')
        if data[2]:
            self.activate()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    sys.exit(app.exec_())