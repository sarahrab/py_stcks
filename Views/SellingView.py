from ViewManager import Transaction, Model
from actions import SelectStockAction, SwitchBackAction
from basics import *
from users import *
from typing import cast


class SellingView(View):
    def get_name(self) -> str:
        return "sell"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        trans = self.data
        if trans:
            print(f"{trans.user.name} total amount: {trans.user.amount}")
            print("select stock to sell: ")
            self.create_menu()

    def create_menu(self):
        t = self.data
        if t and t.user:
            user = t.user # Model.users.find(t.user.name)
            if user:
                self.menu = Menu("menu_sell")
                count = 1
                for stock in t.user.stocks.stocks:
                    self.menu.add_item(MenuItem(stock.to_string(), SelectStockAction("sc", stock, t)))
                    count += 1
                self.menu.add_item(MenuItem("Back", SwitchBackAction(t.user)))
