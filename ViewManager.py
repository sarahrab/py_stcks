import sys

from basics import View, MenuAction
from typing import cast

from stcks import Stocks
from users import UserManager


class ViewManager:
    views = {}

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
            view.data = data
            view.show()
            view.show_menu()
            return True
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
