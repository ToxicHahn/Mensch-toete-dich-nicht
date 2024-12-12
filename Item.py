class Item():
    def __init__(self, name, preis, effekt, beschreibung):
        self._name = name
        self._price = preis
        self._effekt = effekt
        self._beschreibung = beschreibung        
    def holeName(self):
        """Gibt name zurueck."""
        return self._name

    def setzeName(self, value):
        """Setzt name."""
        self._name = value

    def holePreis(self):
        """Gibt preis zurueck."""
        return self._preis

    def setzePreis(self, value):
        """Setzt preis."""
        self._preis = value

    def holeEffekt(self):
        """Gibt effekt zurueck."""
        return self._effekt

    def setzeEffekt(self, value):
        """Setzt effekt."""
        self._effekt = value

    def holeBeschreibung(self):
        """Gibt beschreibung zurueck."""
        return self._beschreibung

    def setzeBeschreibung(self, value):
        """Setzt beschreibung."""
        self._beschreibung = value

