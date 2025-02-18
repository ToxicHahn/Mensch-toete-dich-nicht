from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton,QSpacerItem, QSizePolicy, QScrollArea

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ober_gui(QMainWindow):
    def __init__(self, title, optional_text, width = 800, height = 400):
    
        super().__init__()


        # Fensterkonfiguration
        self.setWindowTitle(title)
        self.setGeometry(100, 100, width, height)
        self.setStyleSheet("background-color: #333333;")
        self.setFixedSize(width,height)

        # Zentrales Widget und Layout
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.central_layout = QVBoxLayout(self.centralwidget)
        self.central_layout.setContentsMargins(20, 20, 20, 20)

        # Header-Layout erstellen
        self.header_layout = QHBoxLayout()
        self.central_layout.addLayout(self.header_layout)

        # Header-Label
        self.header_label = QLabel(title, self)
        self.header_label.setAlignment(Qt.AlignLeft)
        self.header_label.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.header_label.setStyleSheet("color: #FFFFFF; margin-bottom: 20px;")
        self.header_layout.addWidget(self.header_label)
            
        self.optional_text_label = QLabel(optional_text, self)
        self.optional_text_label.setAlignment(Qt.AlignRight)
        self.optional_text_label.setFont(QFont("San Francisco", 24, QFont.Bold))
        self.optional_text_label.setStyleSheet("color: #FFFFFF; margin-left: 450px;")
        self.header_layout.addWidget(self.optional_text_label)

        # Platzhalter für restlichen Header-Inhalt
        self.header_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.header_layout.addSpacerItem(self.header_spacer)

        # Container-Layout (horizontal)
        self.container_layout = QHBoxLayout()
        self.container_layout.setSpacing(10)
        self.central_layout.addLayout(self.container_layout)

    def aktualisiere_optional_text(self, neuer_text):
        """Ermöglicht das Überschreiben des optional_text-Attributs."""
        if not hasattr(self, "optional_text_label"):
            self.optional_text_label = QLabel(neuer_text or "", self)
            self.optional_text_label.setAlignment(Qt.AlignRight)
            self.optional_text_label.setFont(QFont("San Francisco", 24, QFont.Bold))
            self.optional_text_label.setStyleSheet("color: #FFFFFF; margin-left: 450px;")
            self.header_layout.addWidget(self.optional_text_label)
            self.optional_text_label.show()
        elif self.optional_text_label:
            self.optional_text_label.setText(neuer_text)
            self.optional_text_label.show()

    def erstelle_container(self, title, buttons, content_text=None, text_ueber_buttons=None, anpassung_button = None, container_width=150, container_height = 200):
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: #444444;  
                border-radius: 10px;
                margin: 5px;
            }
        """)
        container.setFixedSize(container_width, container_height)

        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)

        # Titel
        title_label = QLabel(title, self)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("San Francisco", 14, QFont.Bold))
        title_label.setStyleSheet("color: #FFFFFF; border: none; margin-top: 10px;")
        layout.addWidget(title_label)

        # Text im Container
        if content_text:
            text_label = QLabel(content_text, self)
            text_label.setAlignment(Qt.AlignCenter)
            text_label.setWordWrap(True)
            text_label.setFont(QFont("San Francisco", 10))
            text_label.setStyleSheet("color: #DDDDDD; border: none; margin: 10px;")
            layout.addWidget(text_label)

        # Optionaler Text über den Buttons
        if text_ueber_buttons:
            text_ueber_buttons_label = QLabel(text_ueber_buttons, self)
            text_ueber_buttons_label.setAlignment(Qt.AlignCenter)
            text_ueber_buttons_label.setFont(QFont("San Francisco", 12))
            text_ueber_buttons_label.setStyleSheet("color: #DDDDDD; margin-bottom: 10px;")
            layout.addWidget(text_ueber_buttons_label)

        # Buttons hinzufügen
        button_layout = QHBoxLayout()
        for button_text, callback in buttons:
            button = QPushButton(button_text)
            button.setStyleSheet(anpassung_button or """
                QPushButton {
                    background-color: #007AFF;
                    color: white;
                    border-radius: 5px;
                    padding: 5px 10px;
                }
                QPushButton:hover {
                    background-color: #005BB5;
                }
            """)
            button.clicked.connect(callback)
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        # Container zum Layout hinzufügen
        self.container_layout.addWidget(container)

    def container_entfernen(self):
        # Entferne alle Widgets aus dem Container-Layout
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()  # Lösche das Widget
            self.container_layout.takeAt(i)  # Entferne den Platzhalter

        # Entferne auch den optionalen Text für die Münzen, falls vorhanden
        #if hasattr(self, "optional_text_label") and self.optional_text_label:
        #    self.optional_text_label.deleteLater()
        #    self.optional_text_label = None

    def erstelle_button(self, text, callback=None, width=None, height=None, angepasst = None):
        button = QPushButton(text)
        button.setFont(QFont("San Francisco", 14, QFont.Bold))
        button.setStyleSheet(angepasst or """
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 10px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        if width:
            button.setFixedWidth(width)
        if height:
            button.setFixedHeight(height)

        if callback:
            button.clicked.connect(callback)

        self.central_layout.addWidget(button, alignment=Qt.AlignCenter)
        return button
    
    def aktualisiere_container(self, title, buttons, content_text=None, text_ueber_buttons=None, minimum_height=None):
        container = self.findChild(QWidget, title)

        if container:
            layout = container.layout()

            for widget in layout.children():
                if isinstance(widget, QLabel):
                    if widget.text() == title:
                        widget.setText(title)
                    elif widget.text() == content_text:
                        widget.setText(content_text)

            button_layout = layout.itemAt(2)
            for button, callback in buttons:
                for button_widget in button_layout.children():
                    if button_widget.text() == button:
                        button_widget.setText(button)
                        button_widget.clicked.disconnect()
                        button_widget.clicked.connect(callback)
                
            container.setMinimumHeight(minimum_height or container.minimumHeight())
            container.update()