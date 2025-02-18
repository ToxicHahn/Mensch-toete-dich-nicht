import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt
from client4 import ClientGUI
from shop import ItemShop
from SPIELFELDD import MenschAergereDichNicht  # Import the new widget

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kombinierte Benutzeroberfläche")
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.setStyleSheet("background-color: #36454F;")

        main_layout = QHBoxLayout(main_widget)

        splitter = QSplitter(Qt.Horizontal)

        self.chat_widget = ClientGUI()
        self.chat_widget.setMinimumWidth(300)
        splitter.addWidget(self.chat_widget)

        middle_widget = QWidget()
        middle_layout = QVBoxLayout(middle_widget)

        self.board_widget = MenschAergereDichNicht("red", "green", "yellow", "blue")
        middle_layout.addWidget(self.board_widget)

        self.shop_widget = ItemShop("player1")
        middle_layout.addWidget(self.shop_widget.gui)

        splitter.addWidget(middle_widget)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        main_layout.addWidget(splitter)

    def resizeEvent(self, event):
        size = min(self.width(), self.height())
        
        self.board_widget.resize(size, size)
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    main_app.show()
    sys.exit(app.exec_())
