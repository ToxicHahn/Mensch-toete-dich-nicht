from PyQt5.QtWidgets import QToolBar, QAction, QVBoxLayout, QSpacerItem, QSizePolicy, QMessageBox, QWidget
from ober_gui import ober_gui
from functools import partial
from shopVariable import VariableShop

class VariableShop_GUI(QWidget):
    def __init__(self, shop, username, connection, parent=None):
        super().__init__(parent)
        
        self.shop = shop
        self.username = username
        self.connection = connection
        self.cursor = self.connection.cursor()

        # Datenbank Verbindungen
        #self.connection = sqlite3.connect(f"databaseN.db")
        #self.cursor = self.connection.cursor()

        # Gems ladwen
        query = f'SELECT gems FROM gem WHERE username == ?;'
        self.cursor.execute(query, (self.username,))
        gem = self.cursor.fetchone()
        self.gems_text = f'Gems: {gem[0]}' if gem else "Gems: 0"
        self.layout = QVBoxLayout(self)
        # GUI initialisieren
        print(self.gems_text)

        self.gui = ober_gui("Shop", self.gems_text)
        self.layout.addWidget(self.gui)

        # Platzhalter hinzufügen, um die Toolbar nach unten zu drücken
        spacer = QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(spacer)

        # Toolbar hinzufügen
        self.add_toolbar()

        # skins
        self.skins = ["skinKrone", "skinSchwarz", "skinLila", "skinRainbow"]
        self.setup_main_shop_view()

    def add_toolbar(self):
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
        self.layout.addWidget(toolbar)

    def back(self):
        parent_widget = self.parent()
        if parent_widget:
            parent_widget.setCurrentIndex(2)

    def setup_main_shop_view(self):
        self.gui.container_entfernen()

        for skin in self.skins:
            query = f'SELECT beschreibung FROM {skin};'
            self.cursor.execute(query)
            beschreibung1 = self.cursor.fetchall()

            beschreibung_text = beschreibung1[0][0] if beschreibung1 else "Keine Beschreibung verfügbar."

            self.gui.erstelle_container(
                title=skin,
                content_text=beschreibung_text,
                buttons=[("Kaufen", partial(self.kaufen, skin))],
                container_height=250,
                container_width=175
            )

    def kaufen(self, skin):
        VariableShop.kaufen(self, skin, self.username)

    def updateGUI(self):
        query = f'SELECT gems FROM gem WHERE username == ?;'
        self.cursor.execute(query, (self.username,))
        gem = self.cursor.fetchone()[0]

        gems_text = f'Gems: {gem}'
        self.gui.aktualisiere_optional_text(gems_text)

    def show_error_message(self, index):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Skin bereits in Besitz!" if index == 0 else "Zu wenig Gems!")
        msg.setWindowTitle("Fehler")
        msg.exec_()