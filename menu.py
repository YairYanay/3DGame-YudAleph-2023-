from ursina import *

class MainMenu(Entity):
    def __init__(self):
        super().__init__()

        self.title = Text(text="Main Menu", y=.5, origin=(0, 0), scale=2)

        self.play_button = Button(text="Play", y=-.1, scale=.15)
        self.play_button.on_click = self.play_game

        self.quit_button = Button(text="Quit", y=-.3, scale=.15)
        self.quit_button.on_click = application.quit

    def play_game(self):
        subprocess.run(["python", "game.py"])


app = Ursina()
main_menu = MainMenu()
app.run()