from basics import *
from users import *
from typing import cast

class LoginView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        username = input("Enter your username:")
        password = input("Enter your password:")
        if username != '' and password != '':
            self.data = User(username, password)

class RegisterUserView(LoginView):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        username = input("Enter your username:")
        password = input("Enter your password:")
        amount = input("Enter your amount:")
        int_amount = int(amount)
        if username != '' and password != '' and int_amount > 0:
            self.data = User(username, password, int_amount)



