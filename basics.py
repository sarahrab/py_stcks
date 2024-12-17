import os
from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")

class MenuAction:
    def __init__(self, data: T | None):
        self.data = data
        self.result = None

    def execute(self):
        pass


class MenuItem:
    def __init__(self, text: str, action: MenuAction):
        self.id = -1
        self.text = text
        self.action = action

    def show(self):
        print(f"{self.id}: {self.text}")

    def execute(self, data: T | None = None):
        self.action.data = data
        self.action.execute()


class Menu:
    def __init__(self, title):
        self.title = title
        self.items = []

    def add_item(self, item: MenuItem):
        self.items.append(item)
        item.id = f"{len(self.items)}"

    def get_item(self, id: str) -> MenuItem | None:
        for item in self.items:
            if item.id == id:
                return item
        return None

    def show(self, data: T | None = None):
        for item in self.items:
            item.show()

    def run(self, data: T | None = None):
        self.show(data)
        item = None
        while item is None:
            option = input()
            item = self.get_item(option)
            #if item is not None:
        item.execute(data)

    def count(self) -> int:
        return len(self.items)


class View:
    subclasses = []

    def __init__(self, menu: Menu = None, data: T | None = None):
        self.menu = menu
        self.data = data

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __new__(cls, name: str):
        for subclass in cls.subclasses:
            if subclass.get_name(name) == name:
                return object.__new__(subclass)
        else:
            return object.__new__(cls)  # Default is this base class.

    @abstractmethod
    def get_name(self) -> str:
        pass


    def show(self):
        pass

    def show_menu(self):
        print()
        if self.menu is not None:
            self.menu.run(self.data)

    @abstractmethod
    def create_menu(self):
        pass


