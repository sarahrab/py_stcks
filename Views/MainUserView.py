from ViewManager import Transaction, Model
from YamlLoader import YamlLoader
from actions import LogoutAction, StartTransactionAction, SwitchViewAction, DeleteAction
from basics import *
from typing import cast

from stocks import Stock
from users import *


class MainUserView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()

        user = None
        if type(self.data) == UserAccount:
            user = cast(UserAccount, self.data)
        else:
            t = cast(Transaction, self.data)
            user = t.user

        if user is not None:
            print(f"Hello again, {user.name}!")
            #user.stocks.add(Stock(agency = "nayax", price = 25, count = 10))  # test only
            #YamlLoader.serialize_users(Model.users, "D:\\python\\py_stcks\\db\\users.yaml")

    def create_menu(self):
        self.menu = Menu("u")
        self.menu.add_item(MenuItem("1", "Check Funds", SwitchViewAction("user_funds")))
        self.menu.add_item(MenuItem("2", "Check Stock", SwitchViewAction("user_stocks")))
        self.menu.add_item(MenuItem("3", "Buy", StartTransactionAction("buy", True)))
        self.menu.add_item(MenuItem("4", "Sell", StartTransactionAction("sell", False)))
        self.menu.add_item(MenuItem("5", "Logout", LogoutAction("welcome")))
        self.menu.add_item(MenuItem("6", "Delete Account", SwitchViewAction("delete")))

