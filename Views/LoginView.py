from actions import LoginAction, SwitchViewAction
from basics import *
from users import *
from typing import cast


class LoginView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        username = input("Enter your username:")
        password = input("Enter your password:")
        if username != '' and password != '':
            self.data = UserAccount(name=username, password=password, amount=0)

    def create_menu(self):
        self.menu = Menu("l")
        self.menu.add_item(MenuItem("Submit", LoginAction("user_main")))
        self.menu.add_item(MenuItem("Cancel", SwitchViewAction("welcome")))


