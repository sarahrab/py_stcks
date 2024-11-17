import sys

from pydantic import BaseModel

from YamlLoader import YamlLoader
from basics import View, MenuAction
from typing import cast, Dict

from singleton import Singleton
from stocks import Stocks, Stock
from users import UserManager


class ViewManager:
    views = {}
    views_stack = []

    @classmethod
    def add_view(cls, view: View):
        v = cls.views.get(view.name, None)
        if v is None:
            cls.views[view.name] = view

    @classmethod
    def switch_view(cls, name: str, data: object | None = None) -> bool:
        v = cls.views.get(name, None)
        if v is not None:
            view = cast(View, v)
            if data is not None:
                view.data = data
            cls.views_stack.append(name)
            print()
            view.show()
            view.show_menu()
            return True
        return False

    @classmethod
    def switch_back(cls, data: object | None = None) -> bool:
        if len(cls.views_stack) > 1:
            cls.views_stack.pop()
            prev = cls.views_stack.pop()
            return cls.switch_view(prev, None)
        return False


class Model(metaclass=Singleton):
    stocks = Stocks()
    users = UserManager()
    error_messages = {}
    stocks_db = ''
    users_db = ''
    error_messages_db = ''

    def initialize(self):
        self.initialize_stocks()
        # s = YamlLoader.deserialize_stocks(Model.stocks_db)
        # if s is not None:
        #     cls.stocks = s
        self.initialize_users()
        # u = YamlLoader.deserialize_users(Model.users_db)
        # if u is not None:
        #     cls.users = u
        self.initialize_error_messages()

    def initialize_stocks(self):
        s = YamlLoader.deserialize_stocks(self.stocks_db)
        if s is not None:
            self.stocks = s

    def initialize_users(self):
        u = YamlLoader.deserialize_users(self.users_db)
        if u is not None:
            self.users = u

    def save_users(self):
        YamlLoader.serialize_users(self.users, self.users_db)

    def save_stock(self):
        YamlLoader.serialize_stocks(self.stocks, self.stocks_db)

    def save(self):
        self.save_stock()
        self.save_users()

    def initialize_error_messages(self):
        self.error_messages = YamlLoader.deserialize_error_messages(self.error_messages_db)


class Transaction:
    def __init__(self):
        self.user = None
        self.stock = None
        self.count = 0
        self.price = 0
        self.error_msg = ""

    def finalize_transaction(self, stocks: Stocks, amount: int):
        stocks.add(Stock(agency=self.stock.agency,
                         price=self.stock.price,
                         count=self.count))
        self.user.amount += amount
        self.error_msg = "success!!!!"

    def execute(self):
        pass

class BuyTransaction(Transaction):
    def __init__(self):
        super().__init__()

    def execute(self):
        if not Model().stocks.remove(self.stock.agency, self.count):
            self.error_msg = "stock BAD"
            return
        self.finalize_transaction(self.user.stocks, -(self.stock.price * self.count))


class SellTransaction(Transaction):
    def __init__(self):
        super().__init__()

    def execute(self):
        if not self.user.stocks.remove(self.stock.agency, self.count):
            self.error_msg = "stock BAD"
            return
        self.finalize_transaction(Model().stocks, self.stock.price * self.count)
