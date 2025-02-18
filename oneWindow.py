import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtGui import QCloseEvent
import sqlite3


class oneWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
    def close(self, username, connection):
        cursor = connection.cursor()
        query = f'UPDATE user SET status == 0 WHERE username == ?;'
        cursor.execute(query, (username,))
        connection.commit()
        connection.close()
