import sys
import os
from PyQt5.QtWidgets import QApplication
from threading import Thread
from yy import Client  # Stelle sicher, dass das Client-Modul korrekt importiert wird

# Setze den Pfad für die Qt-Plattform-Plugins
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\janni\AppData\Local\Programs\Python\Python3.13\Lib\site-packages\PyQt5\Qt\plugins\platforms'

def start_client(player_color):
    """Startet eine Client-Instanz für einen bestimmten Spieler"""
    app = QApplication(sys.argv)
    client = Client(player_color)
    sys.exit(app.exec_())

if __name__ == "__main__":
    # Erstelle 4 verschiedene Threads, um 4 Instanzen von Client zu starten
    threads = []

    # Starten der Client-Instanzen für die Spieler
    for player in ['red', 'green', 'yellow', 'blue']:
        thread = Thread(target=start_client, args=(player,))
        thread.start()
        threads.append(thread)

    # Warten auf alle Threads
    for thread in threads:
        thread.join()
