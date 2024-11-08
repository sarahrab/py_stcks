from basics import *
from users import *
from typing import cast


class StockCountView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        user = cast(UserAccount, self.data)
        if user:
            print(f"{user.name} total amount: {user.amount}")
            count= input("input stock count: ")
