from databasePreGame import DatabasePreGame
from database import Database
import sqlite3

class skin():
    def __init__(self, username, conn):
        super().__init__()

        self.username = username

        self.connection = conn
        self.cursor = self.connection.cursor()

        self.gems_text = ""
        self.skins = ["skinSchwarz", "skinLila", "skinRainbow", "skinKrone"]
        self.beschreibungen = []
        self.istInBesitz = []
        self.kosten = []
        self.index = 0  

    def hole_beschreibung(self):
        if self.index < len(self.skins):
            skins = self.skins[self.index]
            bes = f"SELECT beschreibung FROM {skins};"
            self.cursor.execute(bes)
            result = self.cursor.fetchone()
            beschreibung = result[0] if result else "Keine Beschreibung verfügbar."

            return beschreibung
        else:
            return "Keine weiteren Beschreibungen verfügbar."

    def hole_mengen(self):
        if self.index < len(self.skins):
            skins = self.skins[self.index]
            men = f"SELECT {skins} FROM inventarSkin;"
            self.cursor.execute(men)
            result = self.cursor.fetchone()
            menge = result[0] if result else "Skin ist nicht verfügbar."

            return menge
        else:
            return "Keine Skins verfügbar."

    def hole_kosten(self):
        if self.index < len(self.skins):
            skins = self.skins[self.index]
            kos = f"SELECT kosten FROM {skins};"
            self.cursor.execute(kos)
            result = self.cursor.fetchone()
            kosten = result[0] if result else "Kein Preis verfügbar."

            return kosten
        else:
            return "Keine weiteren Kosten verfügbar."

    def naechster_skin(self, index=None):
        if index is not None:
        # Überprüfen, ob der angegebene Index gültig ist
            if 0 <= index < len(self.skins):
                self.index = index
            else:
                raise ValueError("Ungültiger Index: Der Wert liegt außerhalb des gültigen Bereichs.")
        else:
        # Zum nächsten skins wechseln
            self.index += 1
            if self.index >= len(self.skins):
                self.index = 0