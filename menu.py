from ursina import *
import subprocess
import os

invalid_letters = [' ', ',', '.', '!', '?', '@', '#', '$', '%', '&', '*', '+', '=', ':', ';', '"', "'", r'\\', '/', '|', '<', '>', '[', ']', '{', '}', '~', '`', '^']
class UsernameScreen(Entity):
    def __init__(self):
        super().__init__()

        self.username = ""  # Initialize the username attribute
        self.username_label = Text(text="Username:", x=-0.23 ,y=.21, color=color.gray)
        self.username_input = InputField(y=0.2)
        self.username_input.on_value_changed = self.remove_text_label
        self.submit_button = Button(text="Submit", y=0, scale=(0.3, 0.2))
        self.submit_button.on_click = self.submit_username

        self.quit_button = Button(text="Quit", y=-.3, scale=.15)

    def remove_text_label(self):
        if self.username_input.text:
            self.username_label.enabled = False  # Hide the username label if the username_input has more than one character
        else:
            self.username_label.enabled = True  # Show the username label if the username_input has one or fewer characters

        for i in invalid_letters:
            if i in self.username_input.text:
                error_text = Text(text=f"You cannot use '{i}' in the username.", x=-0.23, y=.15, color=color.red)
                destroy(error_text, delay=1)
                print(f"You cannot use {i} in the username.")
                self.username_input.text = self.username_input.text.replace(f'{i}', '')
        self.username = self.username_input.text

    def submit_username(self):
        print(self.username_input.text)
        self.username = self.username_input.text
        print("Submitted username:", self.username)

    def get_username(self):
        return self.username

class MainMenu(Entity):
    def __init__(self):
        super().__init__()

        self.title = Text(text="Yair 3D Game", y=.4, origin=(0, 0), scale=2)

        self.play_button_1v1 = Button(text="1v1", y=.1, x=0 , scale=.15)
        self.play_button_1v1.on_click = self.play_game1v1

        self.play_button_2v2 = Button(text="2v2", y=-.1 , x=0, scale=.15)
        self.play_button_2v2.on_click = self.play_game_2v2

        self.play_button_3v3 = Button(text="3v3", y=.1, x=-.3, scale=.15)
        self.play_button_3v3.on_click = self.play_game_3v3

        self.play_button_4v4 = Button(text="4v4", y=-.1, x=-.3, scale=.15)
        self.play_button_4v4.on_click = self.play_game_4v4

        self.play_button_5v5 = Button(text="5v5", y=.1, x=.3, scale=.15)
        self.play_button_5v5.on_click = self.play_game_5v5

        self.play_button_6v6 = Button(text="6v6", y=-.1, x=.3, scale=.15)
        self.play_button_6v6.on_click = self.play_game_6v6

        self.quit_button = Button(text="Quit", y=-.3, scale=.15)
        self.quit_button.on_click = application.quit

    def play_game1v1(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(2), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back

    def play_game_2v2(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    with open('names.txt', 'a') as fp:
                        fp.write(f"\n{username}")
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(4), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back

    def play_game_3v3(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    with open('names.txt', 'a') as fp:
                        fp.write(f"\n{username}")
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(6), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back

    def play_game_4v4(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    with open('names.txt', 'a') as fp:
                        fp.write(f"\n{username}")
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(8), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back

    def play_game_5v5(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    with open('names.txt', 'a') as fp:
                        fp.write(f"\n{username}")
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(10), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back

    def play_game_6v6(self):
        username_screen = UsernameScreen()
        self.play_button_1v1.enabled = False
        self.play_button_2v2.enabled = False
        self.play_button_3v3.enabled = False
        self.play_button_4v4.enabled = False
        self.play_button_5v5.enabled = False
        self.play_button_6v6.enabled = False
        self.quit_button.enabled = False
        username_screen.submit_button.enabled = True
        username_screen.username_input.enabled = True

        def on_submit():
            username = username_screen.get_username()
            if username:
                with open('names.txt', 'r') as fp:
                    names = fp.read().split('\n')
                if username not in names:
                    with open('names.txt', 'a') as fp:
                        fp.write(f"\n{username}")
                    print("Username:", username)
                    subprocess.run(["python", "game.py", str(12), username])

                else:
                    print("name catch!")

            else:
                print("you write nothing!")
        def return_back():
            self.play_button_1v1.enabled = True
            self.play_button_2v2.enabled = True
            self.play_button_3v3.enabled = True
            self.play_button_4v4.enabled = True
            self.play_button_5v5.enabled = True
            self.play_button_6v6.enabled = True
            self.quit_button.enabled = True
            username_screen.submit_button.enabled = False
            username_screen.username_input.enabled = False
            username_screen.quit_button.enabled = False
            username_screen.username_label.enabled = False

        username_screen.submit_button.on_click = on_submit
        username_screen.quit_button.on_click = return_back


if not os.path.exists('names.txt'):
    f = open("names.txt", "x")

app = Ursina(borderless=False)
main_menu = MainMenu()
app.run()
