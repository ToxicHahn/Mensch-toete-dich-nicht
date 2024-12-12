from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout

Builder.load_file('game.kv')

class PlayerToken(Widget):
    """Repräsentiert eine Spielfigur."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (40, 40)
        self.pos = (0, 0)  # Startposition

    def move_to(self, x, y):
        self.pos = (x, y)

class GameBoard(Widget):
    """Das Spielfeld mit Feldern und Figuren."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.create_board()
        self.add_tokens()

    def create_board(self):
        """Erstellt ein 11x11 Raster für die Spielfelder."""
        grid = self.ids.field_grid

        for row in range(11):
            for col in range(11):
                # Optional: Setze nur Spielfelder auf bestimmte Positionen
                if (row in [0, 10] or col in [0, 10]) and not (row == col == 0):
                    btn = Button(
                        background_normal="assets/field.png",
                        size_hint=(None, None),
                        size=(50, 50),
                    )
                    grid.add_widget(btn)
                else:
                    grid.add_widget(Widget())  # Leeres Feld

    def add_tokens(self):
        """Fügt Figuren für jeden Spieler hinzu."""
        for i in range(4):
            token = PlayerToken()
            token.move_to(50 * i, 50)  # Beispielposition
            self.add_widget(token)

class MenschArgereDichNichtApp(App):
    def build(self):
        return GameBoard()

if __name__ == '__main__':
    MenschArgereDichNichtApp().run()
