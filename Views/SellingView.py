from ViewManager import Transaction, Model
from actions import SelectStockAction, SwitchBackAction
from basics import *
from users import *
from typing import cast


class SellingView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        trans = cast(Transaction, self.data)
        if trans:
            print(f"{trans.user.name} total amount: {trans.user.amount}")
            print("select stock to sell: ")
            self.create_menu()

    def create_menu(self):
        t = cast(Transaction, self.data)
        if t and t.user:
            user = Model.users.find(t.user.name)
            if user:
                self.menu = Menu("menu_sell")
                count = 1
                for stock in t.user.stocks.stocks:
                    self.menu.add_item(MenuItem(f"{count}", stock.to_string(), SelectStockAction("trans", stock, t)))
                    count += 1
                self.menu.add_item(MenuItem(f"{count}", "Back", SwitchBackAction(t.user)))
