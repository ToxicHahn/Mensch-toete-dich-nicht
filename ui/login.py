from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import sqlite3 as sq
from os import path
from bcrypt import gensalt, hashpw

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster-Eigenschaften
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 250)

        # Layout und zentrale Widget
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)

        # Titel
        self.header = QLabel("Login", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("Arial", 24, QFont.Bold))
        self.header.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.header)

        # Abstand zwischen Header und Formular
        self.layout.addSpacing(20)

        # Eingabefelder für Benutzername und Passwort
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Benutzername")
        self.username_input.setStyleSheet("padding: 10px;")
        
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setStyleSheet("padding: 10px;")

        # Buttons hinzufügen
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 5px;
                font-size: 16px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """)
        self.login_button.clicked.connect(self.login)

        # Layouts zusammenfügen
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)

    def login(self):
        
        username = self.username_input.text()
        password = self.password_input.text()

        db_path = path.join(path.dirname(__file__), '../data/data.db')
        conn = sq.connect(db_path)
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT passwort, salt FROM Accounts WHERE accountName = ?""", (username))
        except:
            print("Error: Account does not exist.")
            raise "Error: Account does not exist."
        dbPass, dbSalt = cursor.fetchone()
        hashedPassword = hashpw(password.encode(), dbSalt)
        conn.close()
            # Beispiel: Benutzername und Passwort überprüfen (diese Logik müsste natürlich aus der DB oder anderen Quellen kommen)
        if hashedPassword==dbPass:
            print("Login erfolgreich!")
            self.close()  # Fenster schließen
        else:
            print("Ungültige Anmeldedaten.")
# Hauptfunktion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
