from actions import LogoutAction, StartTransactionAction, SwitchViewAction
from basics import *

from users import *


class MainUserView(View):
    def get_name(self) -> str:
        return "user_main"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()

        user = None
        if type(self.data) == UserAccount:
            user = self.data
        else:
            user = self.data.user

        if user is not None:
            print(f"Hello again, {user.name}!")
            #user.stocks.add(Stock(agency = "nayax", price = 25, count = 10))  # test only
            #YamlLoader.serialize_users(Model.users, "D:\\python\\py_stcks\\db\\users.yaml")

    def create_menu(self):
        self.menu = Menu("u")
        self.menu.add_item(MenuItem("Check Funds", SwitchViewAction("user_funds")))
        self.menu.add_item(MenuItem("Check Stock", SwitchViewAction("user_stocks")))
        self.menu.add_item(MenuItem("Buy", StartTransactionAction("buy", True)))
        self.menu.add_item(MenuItem("Sell", StartTransactionAction("sell", False)))
        self.menu.add_item(MenuItem("Logout", LogoutAction("welcome")))
        self.menu.add_item(MenuItem("Delete Account", SwitchViewAction("delete")))

