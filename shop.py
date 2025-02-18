import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ober_gui import ober_gui
import sqlite3
from database import Database
from databasePreGame import DatabasePreGame
from functools import partial
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget

class ItemShop(QMainWindow):
    def __init__(self, player):
        super().__init__()

        self.player = player

        # Verbindung nur einmal herstellen und gemeinsam nutzen
        self.connection = sqlite3.connect(f"inventar.db")
        self.cursor = self.connection.cursor()

        self.db = Database(1, self.player)
        self.dbPreGame = DatabasePreGame(1, self.player)

        # Überprüfen, ob Coins vorhanden sind
        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coin = self.cursor.fetchone()
        if coin:
            coins_text = f'Münzen: {coin[0]}'
        else:
            coins_text = "Münzen: 0"

        self.gui = ober_gui("Item - Shop / Inventar", optional_text=coins_text)
        self.updateCoins()
        self.gui.show()

        produkte = ["Freeze", "Bombe", "Atombombe", "Zoll"]
        for item in produkte:
            query = f'SELECT beschreibung FROM {item};'
            self.cursor.execute(query)
            beschreibung1 = self.cursor.fetchone()
            beschreibung_text = beschreibung1[0] if beschreibung1 else "Keine Beschreibung verfügbar."

            self.gui.erstelle_container(
                title=item,
                content_text=beschreibung_text,
                buttons=[
                    ("Kaufen", partial(self.button_kaufen, item)),
                    ("Benutzen", partial(self.button_kaufen, item))
                ],
                text_ueber_buttons="Aktionen:",
                minimum_height=400,
            )

    def button_kaufen(self, item):
        try:
            # Coins des Spielers abrufen
            query = f'SELECT coins FROM coin WHERE username == ?;'
            self.cursor.execute(query, (self.player,))
            coin = self.cursor.fetchone()
            if not coin:
                self.show_error_message(1)  # Zu wenig Münzen
                return
            anzCoins = coin[0]

            # Kosten des Items abrufen
            query = f'SELECT kosten FROM {item.lower()};'
            self.cursor.execute(query)
            kosten = self.cursor.fetchone()
            if not kosten:
                self.show_error_message(1)  # Zu wenig Münzen
                return
            kostenZ = kosten[0]

            if anzCoins >= kostenZ:
                # Inventar und Limits prüfen und aktualisieren
                query = f'SELECT max FROM max{item} WHERE player == ?;'
                self.cursor.execute(query, (self.player,))
                maxi = self.cursor.fetchone()

                query = f'SELECT max FROM {item};'
                self.cursor.execute(query)
                maxi2 = self.cursor.fetchone()

                if maxi and maxi[0] < maxi2[0]:
                    # Coins des Spielers aktualisieren
                    anzCoinsNeu = anzCoins - kostenZ
                    query = f'UPDATE coin SET coins = ? WHERE username == ?;'
                    self.cursor.execute(query, (anzCoinsNeu, self.player))
                    self.connection.commit()

                    # Limit erhöhen
                    maxiNEU = maxi[0] + 1
                    query = f'UPDATE max{item} SET max = ? WHERE player == ?;'
                    self.cursor.execute(query, (maxiNEU, self.player))
                    self.connection.commit()

                    # Inventar aktualisieren
                    query = f'SELECT {item.lower()} FROM inventar WHERE username == ?;'
                    self.cursor.execute(query, (self.player,))
                    inventar = self.cursor.fetchone()
                    if inventar:
                        inventarNeu = inventar[0] + 1
                        query = f'UPDATE inventar SET {item.lower()} = ? WHERE username == ?;'
                        self.cursor.execute(query, (inventarNeu, self.player))
                        self.connection.commit()

                    self.updateGUI()
                else:
                    self.show_error_message(0)  # Inventar voll
            else:
                self.show_error_message(1)  # Zu wenig Münzen
        except sqlite3.Error as e:
            print(f"SQLite Fehler: {e}")
            self.connection.rollback()

    def closeEvent(self, event):
        # Verbindung sauber schließen
        self.connection.close()
        event.accept()

    def show_error_message(self, index):
        window = QWidget()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        if index == 0:
            msg.setText("Inventar voll!")
        elif index == 1:
            msg.setText("Zu wenig Münzen!")
        msg.setWindowTitle("Fehler")
        msg.exec_()

    def updateCoins(self):
        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coins = self.cursor.fetchone()
        return coins[0] if coins else 0

    def updateGUI(self):
        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coin = self.cursor.fetchone()[0]

        coins_text = f'Münzen: {coin}'
        self.gui.update_optional_text(coins_text)


# Hauptprogramm ausführen
if __name__ == "__main__":
    app = QApplication(sys.argv)
    hauptfenster = ItemShop("player1")
    sys.exit(app.exec_())