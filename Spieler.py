from Figur import *
class Spieler():
    def __init__(self, name, ip):
        self._name = name
        self._figuren = [Figur(), Figur(), Figur()]
        self._ip = ip
        
    def holeName(self):
        """Gibt name zurueck."""
        return self._name

    def setzeName(self, value):
        """Setzt name."""
        self._name = value

    def holeIp(self):
        """Gibt ip zurueck."""
        return self._ip

    def setzeIp(self, value):
        """Setzt ip."""
        self._ip = value

    def nutzeItem(self, item):
        pass