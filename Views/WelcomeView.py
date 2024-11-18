from actions import ExitViewAction, SwitchViewAction
from basics import *


class WelcomeView(View):
    def get_name(self) -> str:
        return "welcome"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()
        print("Welcome, friend!")

    def create_menu(self):
        self.menu = Menu("w")
        self.menu.add_item(MenuItem("Login", SwitchViewAction("login")))
        self.menu.add_item(MenuItem("Register", SwitchViewAction("regUser")))
        self.menu.add_item(MenuItem("Exit", ExitViewAction()))
