from ViewManager import Model
from actions import SwitchBackAction
from basics import *
from pie import Pie
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

            if user.stocks.count() > 0:
                Pie.show_stock_pie(user.stocks)


    def create_menu(self):
        self.menu = Menu("s")
        self.menu.add_item(MenuItem("Back", SwitchBackAction()))