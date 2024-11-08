from basics import *
from users import *
from typing import cast

class SellingView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        user = cast(UserAccount, self.data)
        if user:
            print(f"{user.name} total amount: {user.amount}")
            print("select stock to sell: ")

