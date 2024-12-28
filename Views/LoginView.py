from datetime import datetime

from actions import LoginAction, SwitchViewAction
from basics import *
from sql_utils.executer import get_history
from users import *
from typing import cast


class LoginView(View):
    def get_name(self) -> str:
        return "login"

    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()

        # history = get_history(1, self.create_date(2024, 11, 1), self.create_date(2024, 12, 1), 0)

        username = input("Enter your username:")
        password = input("Enter your password:")
        if username != '' and password != '':
            self.data = UserAccount(name=username, password=password, amount=0, level=0, user_id=0)

    def create_menu(self):
        self.menu = Menu("l")
        self.menu.add_item(MenuItem("Submit", LoginAction("user_main")))
        self.menu.add_item(MenuItem("Cancel", SwitchViewAction("welcome")))

    def create_date(self, year: int, month: int, day: int) -> datetime:
        year = input("Enter year:")
        month = input("Enter month:")
        day = input("Enter day:")

        return datetime(int(year), int(month), int(day))

