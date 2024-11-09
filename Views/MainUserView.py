from ViewManager import Transaction, Model
from YamlLoader import YamlLoader
from basics import *
from typing import cast

from stocks import Stock
from users import *


class MainUserView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        use = None
        if type(self.data) == UserAccount:
            user = cast(UserAccount, self.data)
        else:
            t = cast(Transaction, self.data)
            user = t.user

        if user is not None:
            print(f"Hello again, {user.name}!")
            user.stocks.add(Stock(agency = "nayax", price = 25, count = 10))  # test only
            #YamlLoader.serialize_users(Model.users, "D:\\python\\py_stcks\\db\\users.yaml")
