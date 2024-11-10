from typing import List
from pydantic import BaseModel

from stocks import Stocks, Stock


class User(BaseModel):
    name: str
    password: str
    amount: int

    # def __init__(self, name, password, amount: int = 0):
    #     self.name = name
    #     self.password = password
    #     self.amount = amount


class UserAccount(User):
    name: str
    password: str
    amount: int
    logged_in: bool = False
    stocks: Stocks = Stocks()

    # def __init__(self, name, password, amount: int = 0):
    #     super().__init__(name, password, amount)
    #     self.loggedIn = False
    #     self.stocks = Stocks()


class UserManager(BaseModel):
    users: List[UserAccount] = []
    # def __init__(self):
    #     self.users = []

    def find(self, name: str, password: str | None = None) -> UserAccount | None:
        for user in self.users:
            if user.name == name and (password is None or user.password == password):
                return user
        return None

    def add(self, name: str, password: str, amount: int) -> UserAccount | None:
        user = self.find(name, password)
        if user is None:
            user = UserAccount(name= name, password= password, amount= amount)
            self.users.append(user)
        return user

    def remove(self, name: str) -> bool:
        user = self.find(name)
        if user is not None:
            if user.stocks.count() == 0:
                user.logged_in = False
                self.users.remove(user)
                return True
        return False
