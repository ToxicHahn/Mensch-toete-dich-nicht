import sys
import socket
import threading
from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLineEdit, QLabel
from PyQt5.QtGui import QTextCursor, QColor, QTextCharFormat

# Serverdetails
server_ip = 'localhost'
server_port = 5555

class ClientThread(QThread):
    message_received = pyqtSignal(str)  # Signal Hauptt GUI

    def __init__(self, client_socket, parent=None):
        super().__init__(parent)
        self.client_socket = client_socket

    def run(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if message:
                    if message.startswith("/move"):
                        print("Methode MOVE")
                        parts = message.split(' ', 3)
                        print(parts)
                    else:
                        self.message_received.emit(message)
            except Exception as e:
                print(f"Fehler beim Empfangen der Nachricht: {e}")
                self.client_socket.close()
                break


class ClientGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Client Chat")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("""
            background-color: #2d2d2d;
            color: white;
            border: 1px solid #444;
            padding: 5px;
        """)
        self.layout.addWidget(self.text_display)

        self.input_field = QLineEdit(self)
        self.input_field.setStyleSheet("""
            background-color: #444;
            color: white;
            border: 1px solid #666;
            padding: 5px;
        """)
        self.layout.addWidget(self.input_field)

        self.target_field = QLineEdit(self)
        self.target_field.setPlaceholderText("Flüster an (Benutzernamen):")
        self.target_field.setStyleSheet("""
            background-color: #444;
            color: white;
            border: 1px solid #666;
            padding: 5px;
        """)
        self.layout.addWidget(self.target_field)

        self.send_button = QPushButton("Senden", self)
        self.send_button.setStyleSheet("""
            background-color: #5e5e5e;
            color: white;
            border: 1px solid #777;
            padding: 5px;
        """)
        self.layout.addWidget(self.send_button)

        self.send_button.clicked.connect(self.send_message)

        self.setLayout(self.layout)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, server_port))
            print(f"Verbunden mit dem Server {server_ip}:{server_port}.")

            self.receive_thread = ClientThread(self.client_socket)
            self.receive_thread.message_received.connect(self.display_message)
            self.receive_thread.start()

        except Exception as e:
            print(f"Fehler beim Verbinden mit dem Server: {e}")
            self.client_socket.close()

    def set_username(self):
        username = self.username_input.text().strip()
        if username:
            try:
                self.client_socket.send(username.encode('utf-8'))
                print(f"Benutzername '{username}' an den Server gesendet.")
            except Exception as e:
                print(f"Fehler beim Senden des Benutzernamens: {e}")
                self.client_socket.close()

    def send_message(self):
        message = self.input_field.text()
        target_client = self.target_field.text()

        if message:
            if target_client:
                whisper_message = f"/whisper {target_client} {message}"
                self.client_socket.send(whisper_message.encode('utf-8'))
                self.text_display.append(f"Du flüsterst an {target_client}: {message}")
            else:
                try:
                    self.client_socket.send(message.encode('utf-8'))
                    self.text_display.append(f"Du: {message}")
                except Exception as e:
                    print(f"Fehler beim Senden der Nachricht: {e}")
                    self.client_socket.close()

            self.input_field.clear()
            self.target_field.clear()

    def display_message(self, message):
        self.text_display.append(f"Server: {message}")






if __name__ == "__main__":
    app = QApplication(sys.argv)
    client_app = ClientGUI()
    client_app.show()
    sys.exit(app.exec_())
