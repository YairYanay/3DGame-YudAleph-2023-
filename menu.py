from ursina import *
import game

class MainMenu(Entity):
    def __init__(self):
        super().__init__()

        self.title = Text(text="Main Menu", y=.5, origin=(0, 0), scale=2)

        self.play_button = Button(text="1v1", y=-.1, scale=.15)
        self.play_button.on_click = self.play_game

        self.quit_button = Button(text="Quit", y=-.3, scale=.15)
        self.quit_button.on_click = application.quit

    def play_game(self):
        subprocess.run(["python", "game.py", str(2)])


app = Ursina(borderless=False)
main_menu = MainMenu()
app.run()
