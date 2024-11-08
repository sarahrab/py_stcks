from basics import *
from typing import cast

from stocks import Stock
from users import *

class MainUserView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        user = cast(UserAccount, self.data)
        if user is not None:
            print(f"Hello again, {user.name}!")
            user.stocks.add(Stock("nayax", 25, 10))  # test only


