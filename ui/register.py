from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QLabel, QWidget, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sqlite3 as sq
from os import path
from bcrypt import gensalt, hashpw
class RegisterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster-Eigenschaften
        self.setWindowTitle("Account erstellen")
        self.setGeometry(100, 100, 400, 300)

        # Layout und zentrale Widget
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)

        # Titel
        self.header = QLabel("Registrierung", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.header.setStyleSheet("color: #333333;")
        self.layout.addWidget(self.header)

        # Abstand zwischen Header und Formular
        self.layout.addSpacing(30)

        # Formular für die Registrierung
        self.form_layout = QFormLayout()

        # Eingabefelder für Benutzername, Passwort und Bestätigung
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Benutzername")
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Passwort")
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setPlaceholderText("Passwort bestätigen")

        # Formularfelder hinzufügen
        self.form_layout.addRow("Benutzername:", self.username_input)
        self.form_layout.addRow("Passwort:", self.password_input)
        self.form_layout.addRow("Passwort bestätigen:", self.confirm_password_input)

        # Button zum Registrieren
        self.register_button = QPushButton("Registrieren", self)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                font-family: 'San Francisco', sans-serif;
                padding: 12px 0;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        self.register_button.clicked.connect(self.register)

        # Layouts zusammenfügen
        self.layout.addLayout(self.form_layout)
        self.layout.addWidget(self.register_button)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if username and password and confirm_password:
            if password == confirm_password:
                print(f"Benutzer {username} wurde erfolgreich registriert.")
                db_path = path.join(path.dirname(__file__), '../data/data.db')
                conn = sq.connect(db_path)
                cursor = conn.cursor()
                salt = gensalt()
                hashed_password = hashpw(password.encode(), salt)
                cursor.execute("INSERT INTO Accounts (accountName, passwort, salt) VALUES (?, ?, ?)", (username, hashed_password, salt))
                conn.commit()
                conn.close()
                self.close()  # Fenster nach erfolgreicher Registrierung schließen
            else:
                print("Passwörter stimmen nicht überein.")
        else:
            print("Bitte alle Felder ausfüllen.")

# Hauptfunktion
if __name__ == "__main__":
    app = QApplication([])
    register_window = RegisterWindow()
    register_window.show()
    app.exec_()
