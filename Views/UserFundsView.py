from actions import SwitchBackAction
from basics import *
from users import UserAccount
from typing import cast


class UserFundsView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        user = cast(UserAccount, self.data)
        if user:
            print(f"{user.name} funds:")
            print(f"    Available   : {user.amount}")
            print(f"    Stock Value : {user.stocks.get_stocks_value()}")

    def create_menu(self):
        self.menu = Menu("f")
        self.menu.add_item(MenuItem("Back", SwitchBackAction()))

