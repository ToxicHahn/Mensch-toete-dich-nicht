from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QApplication
from Spielfeld import Spielfeld
from Wuerfel_Widget import WuerfelWidget
from Spielfeld_GUI_Widget import PygameWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mensch ärgere dich nicht with Dice")
        self.setGeometry(100, 100, 900, 600)
        
        # Create a Spielfeld instance
        self.spielfeld = Spielfeld()
        
        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QHBoxLayout(central_widget)
        
        # Add PygameWidget and DiceWidget, passing the Spielfeld instance
        self.wuerfelwidget = WuerfelWidget(self.spielfeld)
        self.pygamewidget = PygameWidget(self.spielfeld, self.wuerfelwidget, self)

        
        layout.addWidget(self.pygamewidget)
        layout.addWidget(self.wuerfelwidget)
        
        central_widget.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())