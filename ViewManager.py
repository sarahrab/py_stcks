import sys

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



# class OperationalLogic(object):
#     def __init__(self):
#         self.stocks = Stocks()
#         self.users = UserManager()
#
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(OperationalLogic, cls).__new__(cls)
#             return cls.instance


class Model:
    stocks = Stocks()
    users = UserManager()


class Transaction():
    def __init__(self, is_buying: bool):
        self.user = None
        self.stock = None
        self.is_buying = is_buying
        self.count = 0
        self.price = 0
