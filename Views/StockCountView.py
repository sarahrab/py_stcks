from ViewManager import Transaction
from actions import SwitchViewAction, SwitchBackAction
from basics import *
from users import *
from typing import cast

from utils import Utils


class StockCountView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        transaction = cast(Transaction, self.data)
        if transaction and transaction.user:
            print(f"{transaction.user.name} total amount: {transaction.user.amount}")
            text = "buying" if transaction.is_buying else "selling"
            print(f"{text} : {transaction.stock.agency} for {transaction.stock.price}")
            valid = False
            count = 0
            if transaction.is_buying:
                amount = 0
                while not valid:
                    # amount = self.get_int("input money sum : ")
                    amount = Utils.get_int("input money sum : ")
                    if amount > transaction.user.amount:
                        print("error: not enough money")
                    elif amount <= 0:
                        print("amount is incorrect")
                    else:
                        valid = True
                count = int(amount / transaction.stock.price)
                print(f"{text} : {count} {transaction.stock.agency} for {count * transaction.stock.price}")
            else:
                count = 0
                while not valid:
                    count = Utils.get_int("input stock count : ")
                    if count <= 0:
                        print("error: not valid count")
                    elif count > transaction.stock.count:
                        print("not enough in possession")
                    else:
                        valid = True
                amount = int(count * transaction.stock.price)
                print(f"{text} : {count} {transaction.stock.agency} for {amount}")
            transaction.count = count

    # def get_int(self, element: str) -> int:
    #     value= input(element)
    #     try:
    #         number = int(value)
    #         return  number
    #     except ValueError:
    #         print("invalid format!")
    #         return  0

    def create_menu(self):
        self.menu = Menu("sc")
        self.menu.add_item(MenuItem("1", "Submit", SwitchViewAction("trans")))
        self.menu.add_item(MenuItem("2", "Cancel", SwitchBackAction()))

