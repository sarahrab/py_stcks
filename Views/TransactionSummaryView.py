from actions import TransactionExecuteAction, SwitchBackAction
from basics import *
from users import *
from typing import cast
from ViewManager import *


class TransactionSummaryView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        transaction = self.data
        if transaction:
            print(f"{transaction.user.name} current amount: {transaction.user.amount}")
            text = "buying" if type(transaction) is BuyTransaction else "selling"
            print(f"{text}: {transaction.stock.to_string()}")
            print(f"count: {transaction.count} for {transaction.stock.price} per stock")
            print(f"total transaction price: {transaction.stock.price * transaction.count}")

    def create_menu(self):
        self.menu = Menu("tr")
        self.menu.add_item(MenuItem("Execute", TransactionExecuteAction("result")))
        self.menu.add_item(MenuItem("Cancel", SwitchBackAction()))
