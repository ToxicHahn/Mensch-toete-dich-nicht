from PyQt5.QtWidgets import QWidget, QVBoxLayout
from ober_gui import ober_gui
from functools import partial
from generalShop_GUI import Shop
from Regelwerk_GUI import Regelwerk_GUI
from join_gui import JoinGui

class Menu_GUI(QWidget):
    def __init__(self, username, connection, parent=None):
        super().__init__(parent)

        self.username = username

        self.connection = connection

        self.width = 800
        self.height = 400
        # Layout für das Menu-Widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # ober gui einfügen
        self.gui = ober_gui("Menu", self.username)
        self.layout.addWidget(self.gui)

        # Menüelemente erstellen
        produkte = ["Regelwerk", "Spiel beitreten", "Spiel erstellen", "Shop"]
        for menu in produkte:
            self.gui.erstelle_button(
                text=menu,
                width=300,
                height=50,
                callback=partial(self.button_klick, menu)
                )
                

    def button_klick(self, item):
        parent_widget = self.parent()
        if item == "Shop" and parent_widget:
            shop_widget = Shop(self.username, self.connection, parent=parent_widget)
            parent_widget.addWidget(shop_widget)
            parent_widget.setCurrentWidget(shop_widget)
        elif item == "Regelwerk":
            regelwerk_widget = Regelwerk_GUI(self.username, self.connection, parent=parent_widget)
            parent_widget.addWidget(regelwerk_widget)
            parent_widget.setCurrentWidget(regelwerk_widget)
        elif item == "Spiel beitreten":
            join = JoinGui(self.username, self.connection, 0, self)
            parent_widget.addWidget(join)
            parent_widget.setCurrentWidget(join)
        elif item == "Spiel erstellen":
            join = JoinGui(self.username, self.connection, 1, self)
            parent_widget.addWidget(join)
            parent_widget.setCurrentWidget(join)
