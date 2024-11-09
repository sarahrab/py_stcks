from actions import SwitchBackAction
from basics import *
from users import UserAccount
from typing import cast


class UserStocksView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        user = cast(UserAccount, self.data)
        if user:
            print(f"{user.name} stocks:")
            for stock in user.stocks.stocks:
                print("  " + stock.to_string())
            print(f"Total in stocks: {user.stocks.get_stocks_value()}")


    def create_menu(self):
        self.menu = Menu("s")
        self.menu.add_item(MenuItem("1", "Back", SwitchBackAction()))