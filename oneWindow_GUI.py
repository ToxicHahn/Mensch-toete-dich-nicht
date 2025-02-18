from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtGui import QCloseEvent
from oneWindow import oneWindow

class MainWindow(QMainWindow):
    def __init__(self, username, connection):
        super().__init__()
        
        self.connection = connection
        self.username = username
        self.cursor = self.connection.cursor()

        # Fenster definieren
        self.setWindowTitle("Shop System")
        self.setStyleSheet("background-color: #333333;")
        self.setFixedSize(800, 450)
        
        # Stacked Widget für die Navigation
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Initialisiere Menü (erste Anzeige)
        from menu_GUI import Menu_GUI # type: ignore
        self.menu = Menu_GUI(self.username, self.connection, parent=self.stacked_widget)
        self.stacked_widget.addWidget(self.menu)
        self.stacked_widget.setCurrentWidget(self.menu)

    def closeEvent(self, event: QCloseEvent):
        oneWindow.close(self, self.username, self.connection)