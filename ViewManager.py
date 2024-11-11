import sys

from YamlLoader import YamlLoader
from basics import View, MenuAction
from typing import cast

from stocks import Stocks
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


class Model:
    stocks = Stocks()
    users = UserManager()
    stocks_db = ''
    users_db = ''

    @classmethod
    def initialize(cls):
        cls.initialize_stocks()
        # s = YamlLoader.deserialize_stocks(Model.stocks_db)
        # if s is not None:
        #     cls.stocks = s
        cls.initialize_users()
        # u = YamlLoader.deserialize_users(Model.users_db)
        # if u is not None:
        #     cls.users = u

    @classmethod
    def initialize_stocks(cls):
        s = YamlLoader.deserialize_stocks(Model.stocks_db)
        if s is not None:
            cls.stocks = s

    @classmethod
    def initialize_users(cls):
        u = YamlLoader.deserialize_users(Model.users_db)
        if u is not None:
            cls.users = u


class Transaction:
    def __init__(self, is_buying: bool):
        self.user = None
        self.stock = None
        self.is_buying = is_buying
        self.count = 0
        self.price = 0
        self.error_msg = ""
