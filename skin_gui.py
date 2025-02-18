import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QAction
from ober_gui import ober_gui
import sqlite3
from functools import partial
from yy import Client


class SkinGUI(QWidget):
    def __init__(self, username, connection, parent=None):
        super().__init__(parent)

        self.username = username

        self.connection = connection

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
        self.gui = ober_gui("Shopp", self.username)
        self.layout.addWidget(self.gui)

        # Tool-Bar mit Zurück-Button
        self.add_toolbar()

        # Shop-Kategorien
        self.options = ["Krone", "Schwarz", "Lila", "Rainbow"]
        self.setup_main_skin_view()

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
            parent_widget.setCurrentIndex(1)


    def setup_main_skin_view(self):
        self.gui.container_entfernen()

        for option in self.options:
            table=f'skin{option}'
            query = f'SELECT beschreibung FROM {table};'
            self.cursor.execute(query)
            beschreibung = self.cursor.fetchall()

            self.gui.erstelle_container(
                title=option,
                content_text=beschreibung[0][0],
                buttons=[("Wählen", partial(self.back))],
                container_width=175,
                container_height=300
            )
