from typing import cast

from ViewManager import Model, Transaction
from basics import *
from stocks import Stock


class TransactionResultView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        transaction= cast(Transaction, self.data)
        if transaction:
            print(f"transaction result: {transaction.error_msg}")




