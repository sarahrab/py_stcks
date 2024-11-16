import yaml

from ViewManager import Model
from YamlLoader import YamlLoader
from actions import ExitViewAction, SwitchViewAction
from basics import *
from stocks import Stock
from users import UserAccount


class WelcomeView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        print("Welcome, friend!")

    def create_menu(self):
        self.menu = Menu("w")
        self.menu.add_item(MenuItem("Login", SwitchViewAction("login")))
        self.menu.add_item(MenuItem("Register", SwitchViewAction("regUser")))
        self.menu.add_item(MenuItem("Exit", ExitViewAction()))
