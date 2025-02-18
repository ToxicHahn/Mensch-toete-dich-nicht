from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QPushButton, QToolBar, QAction
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class Regelwerk_GUI(QWidget):  # Von QWidget erben
    def __init__(self, username, connection, parent=None):
        super().__init__(parent)

        # Layout für das Regelwerk-Widget
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tool-Bar mit Zurück-Button
        self.add_toolbar()

        # Titel
        self.title_label = QLabel("Mensch toete dich nicht - Regelwerk", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: white;")
        self.layout.addWidget(self.title_label)

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
            rule_label.setStyleSheet("margin: 20px 0; color: white;")
            self.scroll_layout.addWidget(rule_label)

        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

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
            parent_widget.setCurrentIndex(0)
