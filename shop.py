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
        
        self.db = Database(1)
        self.cursor = self.db.connection.cursor()

        self.db = DatabasePreGame(1)
        self.cursorPreGame = self.db.connection.cursor()

        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coin = self.cursor.fetchall()[0][0]

        coins_text = f'Münzen: {coin}'
        self.gui = ober_gui("Item - Shop / Inventar", optional_text=coins_text)

        self.updateCoins()

        self.gui.show() 

        produkte = ["Freeze", "Bombe", "Atombombe", "Zoll"]

        beschreibungen = []
        
        for item in produkte:
            query = f'SELECT beschreibung FROM {item};'
            self.cursorPreGame.execute(query)
            beschreibung1 = self.cursorPreGame.fetchall()
            beschreibungen.append(beschreibung1)

            beschreibung_text = beschreibung1[0][0] if beschreibung1 else "Keine Beschreibung verfügbar."

            # Button mit Bezug auf das Produkt erstellen
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
        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coin = self.cursor.fetchall()
        anzCoins = coin [0][0]

        iteml = item.lower()
        query = f'SELECT kosten FROM {iteml};'
        self.cursor.execute(query)
        kosten = self.cursor.fetchall()
        kostenZ = kosten[0][0]

        if anzCoins > kostenZ or anzCoins == kostenZ:

            #Limit des Spielers ermitteln
            query = f'SELECT max FROM max{item} WHERE player == ?;'
            self.cursor.execute(query, (self.player,))
            maxi = self.cursor.fetchall()

            #Limit des Items ermitteln
            query = f'SELECT max FROM {item};'
            self.cursor.execute(query)
            maxi2 = self.cursor.fetchall()
            
            if maxi < maxi2:
                #Anzahl Coins des Spielers anpassen
                anzCoinsNeu = anzCoins - kostenZ
                query = f'UPDATE coin SET coins = {anzCoinsNeu} WHERE username == ?;'
                self.cursor.execute(query, (self.player,))

                query = f'SELECT coins FROM coin WHERE username == ?;'
                self.cursor.execute(query, (self.player,))
                coin = self.cursor.fetchall()
                print(f'HHH{coin}')
                
                self.updateGUI()
                
                #Limit des Spieler erhöhen
                maxiNEU = maxi[0][0] + 1
                query = f'UPDATE max{item} SET max = {maxiNEU} WHERE player == ?;'
                self.cursor.execute(query, (self.player,))

                #Check
                query = f'SELECT max FROM max{item} WHERE player == ?;'
                self.cursor.execute(query, (self.player,))
                maxi = self.cursor.fetchall()

                #Inventar holen
                iteml = item.lower()
                query = f'SELECT {iteml} FROM inventar WHERE username == ?;'
                self.cursor.execute(query, (self.player,))
                maxi = self.cursor.fetchall()

                #Inventar updaten
                maxiNEU = maxi[0][0] + 1
                query = f'UPDATE inventar SET {iteml} = {maxiNEU} WHERE username == ?;'
                self.cursor.execute(query, (self.player,))

                #Check
                query = f'SELECT {item} FROM inventar WHERE username == ?;'
                self.cursor.execute(query, (self.player,))
                maxi = self.cursor.fetchall()

            elif maxi == maxi2:
                self.show_error_message(0)

        elif anzCoins < kostenZ:
            self.show_error_message(1)

    def closeEvent(self, event):
        self.db.close_connection()
        event.accept()

    def show_error_message(self, index):
        # Erstelle ein Fenster
        window = QWidget() 

        # Erstelle eine QMessageBox für den Fehler
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
        self.cursorPreGame.execute(query, (self.player,))
        coins = self.cursorPreGame.fetchall()
        coinsRN = coins[0][0]
        
        return coinsRN

    def updateGUI(self):
        query = f'SELECT coins FROM coin WHERE username == ?;'
        self.cursor.execute(query, (self.player,))
        coin = self.cursor.fetchall()[0][0]

        coins_text = f'Münzen: {coin}'
        self.gui.update_optional_text(coins_text)

        produkte = ["Freeze", "Bombe", "Atombombe", "Zoll"]
        beschreibungen = []
        for item in produkte:
            query = f'SELECT beschreibung FROM {item};'
            self.cursorPreGame.execute(query)
            beschreibung1 = self.cursorPreGame.fetchall()
            beschreibungen.append(beschreibung1)

            beschreibung_text = beschreibung1[0][0] if beschreibung1 else "Keine Beschreibung verfügbar."

            self.gui.aktualisiere_container(
                title=item,
                content_text=beschreibung_text,
                buttons=[("Kaufen", partial(self.button_kaufen, item))],
                text_ueber_buttons="Aktionen:",
                minimum_height=400,
            )

        self.gui.show()


# Hauptprogramm ausführen
if __name__ == "__main__":
    app = QApplication(sys.argv)
    hauptfenster = ItemShop("player1")
    sys.exit(app.exec_())