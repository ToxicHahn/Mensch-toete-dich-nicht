import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QAction, QMessageBox
from ober_gui import ober_gui
import sqlite3
from functools import partial
from skin_gui import SkinGUI
from yy import Client
from server import Server
import threading
import socket



class JoinGui(QWidget):
    def __init__(self, username, connection, host, parent=None):
        super().__init__(parent)

        self.username = username
        self.host = host
        if self.host == 1:
            self.server_thread = threading.Thread(target=self.start_server, daemon=True)
            self.server_thread.start()

        self.connection = connection
        self.buttons = []
        self.connection = sqlite3.connect(f"databaseN.db")
        self.cursor = self.connection.cursor()
        # Datenbankverbindungen
        #self.db = Database(0, self.username)
        #self.cursor = self.db.connection.cursor()
        #self.dbPreGame = DatabasePreGame(1, self.username)
        #self.cursorPreGame = self.dbPreGame.connection.cursor()

        # Hauptlayout für das Shop-Widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # GUI-Einrichtung
        self.gui = ober_gui("Farbwahl", self.username)
        self.layout.addWidget(self.gui)

        # Tool-Bar mit Zurück-Button
        self.add_toolbar()

        # Shop-Kategorien
        self.options = ["red", "green", "blue", "yellow", "skins"]
        self.setup_main_join_view()

    def start_server(self):
        ip_adresse = socket.gethostbyname(socket.gethostname())
        server = Server(ip_adresse)
        server.start_server()

    def add_toolbar(self):
        """Erstellt eine Tool-Bar mit Zurück-Button."""
        toolbar = QToolBar("Navigation")
        back_action = QAction("Zurück", self)
        back_action.triggered.connect(self.back)
        toolbar.setStyleSheet("""
            QToolBar QToolButton {
                background-color: white;
                color: black;
                font-weight: bold;
                border-radius: 10px;  
                padding: 5px 15px;     
                border: 1px solid black; 
            }""")
        toolbar.addAction(back_action)

        # Tool-Bar als Widget hinzufügen
        self.layout.addWidget(toolbar)

    def back(self):
        parent_widget = self.parent()
        if parent_widget:
            # Hier sicherstellen, dass wir zum Shop zurückkehren
            # Wenn das Widget ein StackedWidget ist und Shop an Index 0 ist, dann setCurrentWidget
            parent_widget.setCurrentIndex(0)  # Wechselt zurück zum Shop


    def setup_main_join_view(self):
        farben = ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FFFFFF"]
        hover_farben = ["#880000", "#008800", "#00008B", "#888800", "#808080"]
        for option, farbe, hover_farbe in zip(self.options, farben, hover_farben):
            angepasst = f"""
                QPushButton {{
                    background-color: {farbe};
                    color: black;
                    border-radius: 10px;
                    padding: 10px;
                }}
                QPushButton:hover {{
                    background-color: {hover_farbe};
                }}
            """
            x =self.gui.erstelle_button(
                text=option,
                width=300,
                height=50,
                angepasst=angepasst,
                callback=partial(self.display_color_content, option)
            )
            self.buttons.append(x)
            print(self.buttons)

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Fehler")
        msg.exec_()


    def display_color_content(self, option):
        parent_widget = self.parent()
        button = self.sender()
        try:
            if parent_widget and not option == "skins":
                button.setEnabled(False)
                ip_adresse = socket.gethostbyname(socket.gethostname())
                self.Client = Client(option)
            else:
                skinGUI = SkinGUI(self.username, self.connection)
                parent_widget.addWidget(skinGUI)
                parent_widget.setCurrentWidget(skinGUI)
        except:
            button.setEnabled(True)
            m = f'Netzwerkfehler! Keine offenen Spiele im lokalen Netzwerk!'
            self.show_error_message(m)