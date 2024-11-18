from abc import abstractmethod
from typing import TypeVar, Generic

T = TypeVar("T")

class MenuItem:
    def __init__(self, text: str):
        self.id = -1
        self.text = text

    def show(self):
        print(f"{self.id}: {self.text}")


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

    def count(self) -> int:
        return len(self.items)


class View:
    subclasses = []

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)

    def __init__(self, menu: Menu = None, data: T | None = None):
        self.menu = menu
        self.data = data

    def __new__(cls, name: str):
        """ Create instance of appropriate subclass. """
        for subclass in cls.subclasses:
            if subclass.get_name(name) == name:
                return object.__new__(subclass)
        else:
            return object.__new__(cls)  # Default is this base class.

    @abstractmethod
    def get_name(self) -> str:
        return "view"

    def show(self):
        pass

    def show_menu(self):
        print()
        if self.menu is not None:
            self.menu.run(self.data)

    def create_menu(self):
        pass


class WelcomeView(View):
    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def get_name(self) -> str:
        return "welcome"

    def show(self):
        self.create_menu()
        print("Welcome, friend!")

    def create_menu(self):
        self.menu = Menu("w")
        self.menu.add_item(MenuItem("Login"))
        self.menu.add_item(MenuItem("Register"))
        self.menu.add_item(MenuItem("Exit"))



class LoginView(View):
    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()
        username = input("Enter your username:")
        password = input("Enter your password:")
        # if username != '' and password != '':
        #     self.data = UserAccount(name=username, password=password, amount=0)

    def create_menu(self):
        self.menu = Menu("l")
        self.menu.add_item(MenuItem("Submit"))
        self.menu.add_item(MenuItem("Cancel"))

    def get_name(self) -> str:
        return "login"
