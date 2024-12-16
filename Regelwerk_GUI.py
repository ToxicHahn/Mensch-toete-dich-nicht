from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QScrollArea, QPushButton, QStatusBar
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Fenster-Eigenschaften
        self.setWindowTitle("Regelwerk - Mensch ärgere dich nicht")
        self.setGeometry(100, 100, 800, 600)

        # Hauptlayout
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Titel
        self.title_label = QLabel("Mensch ärgere dich nicht - Regelwerk", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.main_layout.addWidget(self.title_label)

        # Scroll-Bereich für Regeln
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        # Regeltexte (zentrierte Darstellung und größere Abstände)
        rules = [
            "1. Ziel des Spiels ist es, alle eigenen Figuren ins Ziel zu bringen.",
            "2. Jede Spielfigur beginnt auf einem der vier Startfelder.",
            "3. Ein Spieler würfelt mit einem Würfel, um seine Figuren zu bewegen.",
            "4. Eine Figur kann nur dann in das Ziel einziehen, wenn sie das Feld erreicht.",
            "5. Wenn eine Figur auf ein Feld zieht, auf dem eine andere Figur steht, wird diese Figur zurückgesetzt.",
            "6. Ein Spieler muss immer ziehen, wenn er eine Zahl würfelt.",
            "7. Der Spieler, der als erstes alle Figuren im Ziel hat, gewinnt."
        ]

        for rule in rules:
            rule_label = QLabel(rule, self)
            rule_label.setWordWrap(True)
            rule_label.setAlignment(Qt.AlignCenter)
            rule_label.setFont(QFont("Arial", 18))
            rule_label.setStyleSheet("margin: 20px 0;")
            self.scroll_layout.addWidget(rule_label)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Schließen-Button
        self.close_button = QPushButton("Schließen", self)
        self.close_button.setFont(QFont("Arial", 16))
        self.close_button.setStyleSheet("padding: 10px; background-color: #007AFF; color: white; border-radius: 5px;")
        self.close_button.clicked.connect(self.close)
        self.main_layout.addWidget(self.close_button, alignment=Qt.AlignRight)

        # Statusleiste
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

# Hauptfunktion
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
