from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget
from database import Database
from login import Login as Login
import socket

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster definieren
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 350)

        # Datenbank mit Neustart
        self.db = Database(1)
        self.connection = sqlite3.connect(f"databaseN.db")
        self.cursor = self.connection.cursor()

        # Hintergrundfarbe
        self.setStyleSheet("background-color: #1e1e2e;")

        # centralWidget definieren und ins Layout einfügfen
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)

        # Überschrift
        self.header = QLabel("Login", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("Comic Sans MS", 28, QFont.Bold))
        self.header.setStyleSheet("color: #FFFFFF; margin-bottom: 20px; text-shadow: 2px 2px 4px #000000;")
        self.layout.addWidget(self.header)

        # Fehleranzeige
        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setFont(QFont("Arial", 12))
        self.error_label.setStyleSheet("color: #FF0000; background-color: #330000; border-radius: 5px; padding: 5px;")
        self.error_label.hide()
        self.layout.addWidget(self.error_label)

        # Eingabefelder für Benutzername und Passwort
        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Benutzername")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #FFCCCC;
                color: #333333;
                border: 2px solid #FF6666;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #FF0000;
            }
        """)
        
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Passwort")
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #CCFFCC;
                color: #333333;
                border: 2px solid #66FF66;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #00CC00;
            }
        """)

        # Buttons hinzufügen
        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #CCCCFF;
                color: white;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
                border: 2px solid #6666FF;
            }
            QPushButton:hover {
                background-color: #9999FF;
            }
            QPushButton:pressed {
                background-color: #6666FF;
            }
        """)
        self.login_button.clicked.connect(self.loginGUI)

        # Sign-up Text
        self.signup_label = QLabel("Don't have an account? <a href='#'>Sign up here.</a>", self)
        self.signup_label.setAlignment(Qt.AlignCenter)
        self.signup_label.setFont(QFont("Comic Sans MS", 10))
        self.signup_label.setStyleSheet("color: #FFFF66; margin-top: 10px; text-decoration: none;")
        self.signup_label.setOpenExternalLinks(False)

        # Layouts zusammenfügen
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.login_button)
        self.layout.addWidget(self.signup_label)

    def loginGUI(self):
        username = self.username_input.text()
        passwort = self.password_input.text()
        Login.login(self, username, passwort)
           

    def show_error_message(self, index):
        if index == 0:
            self.error_label.setText("Username existiert nicht!")
        elif index == 1:
            self.error_label.setText("Passwort ist falsch!")
        elif index ==2:
            self.error_label.setText("User aktuell angemeldet!")
        self.error_label.show()

# Hauptfunktion
if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
