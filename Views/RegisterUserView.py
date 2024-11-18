from Views.LoginView import LoginView
from actions import SwitchViewAction, RegisterAction
from basics import View, Menu, MenuItem
from users import UserAccount
from utils import Utils


class RegisterUserView(View):
    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def get_name(self) -> str:
        return "regUser"

    def show(self):
        self.create_menu()
        username = input("Enter your username:")
        password = input("Enter your password:")
        #amount = input("Enter your amount:")
        #int_amount = int(amount)
        int_amount = Utils.get_int("Enter your amount:")
        if username != '' and password != '' and int_amount > 0:
            self.data = UserAccount(name=username, password=password, amount=int_amount)

    def create_menu(self):
        self.menu = Menu("r")
        self.menu.add_item(MenuItem("Submit", RegisterAction("user_main")))
        self.menu.add_item(MenuItem("Cancel", SwitchViewAction("welcome")))