from ViewManager import Transaction, Model
from actions import SelectStockAction, SwitchViewAction, SwitchBackAction
from basics import *
from sql_utils.executer import get_stocks
from sql_utils.models import stock_to_string
from users import *
from typing import cast

class BuyingView(View):
    def get_name(self) -> str:
        return "buy"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        #t = cast(Transaction, self.data)
        if self.data:
            print(f"{self.data.user.name} total amount: {self.data.user.amount}")
            print("Select stock to buy: ")
            self.create_menu()

    def create_menu(self):
        transaction = self.data
        if transaction:
            self.menu = Menu("menu_buy")
            count = 1

            res = get_stocks()
            if res.error == 0 and res.payload is not None:
                for stock in res.payload:
                    self.menu.add_item(MenuItem(stock_to_string(stock), SelectStockAction("sc", stock, transaction)))

            for stock in Model().stocks.stocks:
                self.menu.add_item(MenuItem(stock.to_string(), SelectStockAction("sc", stock, transaction)))
                count += 1
            self.menu.add_item(MenuItem("Back", SwitchBackAction(transaction.user)))
