from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QLabel, QStackedWidget, QHBoxLayout, QStatusBar, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster-Eigenschaften
        self.setWindowTitle("Mensch töte dich nicht! SHOP")
        self.setGeometry(100, 100, 800, 600)

        # Haupt-Widget und Layout
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)

        # Header-Bereich hinzufügen
        self.header_layout = QHBoxLayout()
        self.layout.addLayout(self.header_layout)

        # Zurück-Button
        self.back_button = QPushButton("Zurück")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #D3D3D3;
                color: black;
                border-radius: 5px;
                font-size: 12px;
                padding: 5px 10px;
                border: 1px solid #A9A9A9;
            }
            QPushButton:hover {
                background-color: #C0C0C0;
            }
            QPushButton:pressed {
                background-color: #A9A9A9;
            }
        """)
        self.back_button.setVisible(False)  # Versteckt im Hauptmenü
        self.back_button.clicked.connect(lambda: self.switch_page(0))
        self.header_layout.addWidget(self.back_button, alignment=Qt.AlignLeft)

        # Stretch zwischen Button und Header
        self.header_layout.addStretch()

        # Header
        self.header = QLabel("Mensch töte dich nicht! - SHOP", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.header.setStyleSheet("color: #333333; padding: 10px;")
        self.header.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.header_layout.addWidget(self.header, alignment=Qt.AlignCenter)

        # Stretch nach dem Header
        self.header_layout.addStretch()

        # QStackedWidget für wechselnde Inhalte
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Seiten hinzufügen
        self.main_menu = self.create_main_menu()
        self.item_shop = self.create_item_shop()
        self.skin_shop = self.create_skin_shop()
        self.map_shop = self.create_map_shop()
        self.marketplace = self.create_marketplace()

        self.stacked_widget.addWidget(self.main_menu)  # Seite 0
        self.stacked_widget.addWidget(self.item_shop)  # Seite 1
        self.stacked_widget.addWidget(self.skin_shop)  # Seite 2
        self.stacked_widget.addWidget(self.map_shop)  # Seite 3
        self.stacked_widget.addWidget(self.marketplace)  # Seite 4

        # Statusleiste
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def create_main_menu(self):
        """Erstelle die Hauptmenü-Seite."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Buttons
        self.create_button(layout, "Item SHOP", lambda: self.switch_page(1))
        self.create_button(layout, "Skin SHOP", lambda: self.switch_page(2))
        self.create_button(layout, "Map SHOP", lambda: self.switch_page(3))
        self.create_button(layout, "Marketplace", lambda: self.switch_page(4))

        return page

    def create_item_shop(self):
        """Erstelle die Item SHOP-Seite."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Stretch nach oben, um den Button nach unten zu verschieben
        layout.addStretch()

        # Inhalte des Item-Shops
        self.create_button(layout, "Kaufen", lambda: self.show_message("Kauf abgeschlossen!"))

        return page
    
    def create_skin_shop(self):
        """Erstelle die Skin SHOP-Seite."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Stretch nach oben, um den Button nach unten zu verschieben
        layout.addStretch()

        # Inhalte des Item-Shops
        self.create_button(layout, "Kaufen", lambda: self.show_message("Kauf abgeschlossen!"))

        return page
    
    def create_map_shop(self):
        """Erstelle die Map SHOP-Seite."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Stretch nach oben, um den Button nach unten zu verschieben
        layout.addStretch()

        # Inhalte des Item-Shops
        self.create_button(layout, "Kaufen", lambda: self.show_message("Kauf abgeschlossen!"))

        return page
    
    def create_marketplace(self):
        """Erstelle die Marketplace-Seite."""
        page = QWidget()
        layout = QVBoxLayout(page)

        # Stretch nach oben, um den Button nach unten zu verschieben
        layout.addStretch()

        # Inhalte des Item-Shops
        self.create_button(layout, "Kaufen", lambda: self.show_message("Kauf abgeschlossen!"))

        return page
    
    def create_button(self, layout, text, callback):
        """Hilfsfunktion zum Erstellen von Buttons."""
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 10px;
                font-size: 30px;
                font-family: 'San Francisco', sans-serif;
                padding: 12px 0;
                border: none;
                text-align: center;
            }
            QPushButton:hover {
                background-color: #005BB5;
            }
            QPushButton:pressed {
                background-color: #003F87;
            }
        """)
        button.setMinimumHeight(50)
        layout.addWidget(button)
        button.clicked.connect(callback)

    def switch_page(self, index):
        """Wechsel zwischen Seiten im QStackedWidget."""
        self.stacked_widget.setCurrentIndex(index)

        # Steuerung der Sichtbarkeit des Zurück-Buttons
        self.back_button.setVisible(index != 0)

        # Header-Titel aktualisieren
        if index == 0:
            self.header.setText("Mensch ärgere dich nicht! - SHOP")
        elif index == 1:
            self.header.setText("Mensch ärgere dich nicht! - Item SHOP")
        elif index == 2:
            self.header.setText("Mensch ärgere dich nicht! - Skin SHOP")
        elif index == 3:
            self.header.setText("Mensch ärgere dich nicht! - Map SHOP")
        elif index == 4:
            self.header.setText("Mensch ärgere dich nicht! - Marketplace")

    def show_message(self, message):
        """Zeige eine Nachricht in der Statusleiste."""
        self.statusbar.showMessage(message, 3000)


# Hauptfunktion
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
