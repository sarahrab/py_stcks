from ViewManager import Transaction, Model
from actions import SelectStockAction, SwitchViewAction, SwitchBackAction
from basics import *
from users import *
from typing import cast

class BuyingView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        t = cast(Transaction, self.data)
        if t:
            print(f"{t.user.name} total amount: {t.user.amount}")
            print("Select stock to buy: ")
            self.create_menu()

    def create_menu(self):
        t = cast(Transaction, self.data)
        if t:
            self.menu = Menu("menu_buy")
            count = 1
            for stock in Model().stocks.stocks:
                self.menu.add_item(MenuItem(stock.to_string(), SelectStockAction("sc", stock, t)))
                count += 1
            self.menu.add_item(MenuItem("Back", SwitchBackAction(t.user)))
