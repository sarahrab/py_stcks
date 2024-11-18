from actions import SwitchBackAction
from basics import *
from Utils.pie import Pie


class UserStocksView(View):
    def get_name(self) -> str:
        return "user_stocks"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()
        user = self.data
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
