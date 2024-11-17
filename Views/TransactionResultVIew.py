from typing import cast

from ViewManager import Model, Transaction
from actions import CloseTransactionAction
from basics import *
from stocks import Stock


class TransactionResultView(View):
    def get_name(self) -> str:
        return "result"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()
        transaction=self.data
        if transaction:
            print(f"transaction result: {transaction.error_msg}")

    def create_menu(self):
        self.menu = Menu("r")
        self.menu.add_item(MenuItem("Continue", CloseTransactionAction("user_main")))



