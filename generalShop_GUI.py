import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QToolBar, QAction
from ober_gui import ober_gui
import sqlite3
from functools import partial
from shopVariable_GUI import VariableShop_GUI


class Shop(QWidget):
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
        self.gui = ober_gui("Shop", self.username)
        self.layout.addWidget(self.gui)

        # Tool-Bar mit Zurück-Button
        self.add_toolbar()

        # Shop-Kategorien
        self.shops = ["skin", "map", "marketplace"]
        self.setup_main_shop_view()

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


    def setup_main_shop_view(self):

        for shop in self.shops:
            query = f'SELECT beschreibung FROM shop WHERE shop == ?;'
            self.cursor.execute(query, (shop,))
            beschreibung1 = self.cursor.fetchall()

            beschreibung_text = beschreibung1[0][0] if beschreibung1 else "Keine Beschreibung verfügbar."

            self.gui.erstelle_button(
                text=shop,
                callback=partial(self.display_shop_content,shop),
                width=300,
                height=65
            )

    def display_shop_content(self, shop):
        parent_widget = self.parent()
        if parent_widget and shop == "skin":
            variable_shop = VariableShop_GUI(shop, self.username, self.connection, parent=parent_widget)
            parent_widget.addWidget(variable_shop)
            parent_widget.setCurrentWidget(variable_shop)