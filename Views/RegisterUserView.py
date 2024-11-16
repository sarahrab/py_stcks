from Views.LoginView import LoginView
from actions import SwitchViewAction, RegisterAction
from basics import View, Menu, MenuItem
from users import UserAccount
from utils import Utils


class RegisterUserView(LoginView):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

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