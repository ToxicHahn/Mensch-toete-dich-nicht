from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton, QStatusBar, QMenuBar, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QFont
from Regelwerk_GUI import MainWindow as RegelwerkWindow  

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    
        self.regelwerk_fenster = None 

        # Fenster-Eigenschaften
        self.setWindowTitle("Mensch ärgere dich nicht! Launcher")
        self.setGeometry(100, 100, 600, 400)

        # Fensterlayout und zentrale Widget
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(30, 30, 30, 30)

        # Header (Titelbereich)
        self.header = QLabel("Mensch ärgere dich nicht!", self)
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.header.setStyleSheet("color: #333333;")
        self.central_layout.addWidget(self.header)

        # Abstand zwischen Header und Buttons
        self.central_layout.addSpacing(30)

        # Buttons
        self.create_button("Spiel beitreten")
        self.create_button("Spiel hosten")
        self.create_button("Account erstellen")
        self.create_button("Login")
        self.create_button("Regelwerk anzeigen")  

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

        if text == "Regelwerk anzeigen":
            button.clicked.connect(self.open_regelwerk)  
        else:
            button.clicked.connect(self.on_button_click)

    def create_menu(self):
        menubar = self.menuBar()
        settings_menu = menubar.addMenu('Settings')

        settings_action = QAction('Toggle Dark Mode', self)
        settings_action.triggered.connect(self.toggle_dark_mode)
        settings_menu.addAction(settings_action)

        settings_action_ = QAction('Toggle White Mode', self)
        settings_action_.triggered.connect(self.toggle_white_mode)
        settings_menu.addAction(settings_action_)

    def toggle_dark_mode(self):
        """Wechsel zwischen Light und Dark Mode"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(28, 28, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.black)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.black)
        dark_palette.setColor(QPalette.Base, QColor(42, 42, 42))
        dark_palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)

        self.setPalette(dark_palette)

    def toggle_white_mode(self):
        white_palette = QPalette()
        white_palette.setColor(QPalette.Window, QColor(255, 255, 255))
        white_palette.setColor(QPalette.WindowText, Qt.black)
        white_palette.setColor(QPalette.Button, QColor(240, 240, 240))
        white_palette.setColor(QPalette.ButtonText, Qt.black)
        white_palette.setColor(QPalette.Base, QColor(255, 255, 255))
        white_palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        white_palette.setColor(QPalette.ToolTipBase, Qt.black)
        white_palette.setColor(QPalette.ToolTipText, Qt.black)
        white_palette.setColor(QPalette.Text, Qt.black)
        white_palette.setColor(QPalette.BrightText, Qt.red)

        self.setPalette(white_palette)

    def on_button_click(self):
        sender = self.sender()
        self.statusbar.showMessage(f"{sender.text()} Button Clicked")

    def open_regelwerk(self):
        """Öffnet das Regelwerk-Fenster, falls noch nicht geöffnet"""
        if self.regelwerk_fenster is None or not self.regelwerk_fenster.isVisible():  
            self.regelwerk_fenster = RegelwerkWindow()  
            self.regelwerk_fenster.show()  

    def reset_regelwerk_fenster(self):
        """Setzt das Regelwerk-Fenster auf None, wenn es geschlossen wird."""
        self.regelwerk_fenster = None

# Hauptfunktion
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
