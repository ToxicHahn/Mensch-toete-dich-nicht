from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QMenuBar, QAction, QStatusBar, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette, QFont

class itemSHOP(QMainWindow):
    def __init__(self):
        super().__init__()
        print("1")

        # Fenster-Eigenschaften
        self.setWindowTitle("Mensch ärgere dich nicht! SHOP1")
        self.setGeometry(100, 100, 600, 400)
        print("2")

        # Fensterlayout und zentrale Widget
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(30, 30, 30, 30)  # Abstand zum Rand

        # Header (Titelbereich)
        self.header = QLabel("Mensch töte dich nicht! - SHOP", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.header.setStyleSheet("color: #333333;")
        self.central_layout.addWidget(self.header)

        # Abstand zwischen Header und Buttons
        self.central_layout.addSpacing(30)

        # Buttons
        self.create_button("Item SHOP")
        self.create_button("Skin SHOP")
        self.create_button("Map SHOP")
        self.create_button("Marketplace")

        # Menüleiste erstellen
        self.create_menu()

        # Statusleiste
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    def create_button(self, text):
        button = QPushButton(text)
        button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF;
                color: white;
                border-radius: 10px;
                font-size: 16px;
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
        self.central_layout.addWidget(button)
        button.clicked.connect(self.on_button_click)

    def create_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('Settings')

        settings_action = QAction('Toggle Dark Mode', self)
        settings_action.triggered.connect(self.toggle_dark_mode)
        settings_menu.addAction(settings_action)

    def toggle_dark_mode(self):
        """Wechsel zwischen Light und Dark Mode"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(28, 28, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        self.setPalette(dark_palette)

    def on_button_click(self):
        sender = self.sender()
        self.statusbar.showMessage(f"{sender.text()} Button Clicked")
        print(sender.text())
        if sender.text() == "Item SHOP":
            self.destroy()
        elif sender.text() == "Skin SHOP":
            pass
        elif sender.text() == "Map SHOP":
            pass
        elif sender.text() == "Marketplace":
            pass
# Hauptfunktion
if __name__ == "__main__":
    app = QApplication([])
    window = itemSHOP()
    window.show()
    app.exec_()
