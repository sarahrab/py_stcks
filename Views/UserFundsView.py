from actions import SwitchBackAction
from basics import *
from users import UserAccount
from typing import cast


class UserFundsView(View):
    def get_name(self) -> str:
        return "user_funds"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()
        user = self.data
        if user:
            print(f"{user.name} funds:")
            print(f"    Available   : {user.amount}")
            print(f"    Stock Value : {user.stocks.get_stocks_value()}")

    def create_menu(self):
        self.menu = Menu("f")
        self.menu.add_item(MenuItem("Back", SwitchBackAction()))

