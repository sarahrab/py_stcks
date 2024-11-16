from typing import cast

from ViewManager import ViewManager
from actions import DeleteAction, SwitchBackAction
from basics import View, Menu, MenuItem
from users import UserAccount


class DeleteView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        self.create_menu()
        user = cast(UserAccount, self.data)
        if user:
            if user.stocks.count() > 0:
                print("You have to sell all your stocks!")
                ViewManager.switch_back()
            else:
                print("Please, confirm the delete:")

    def create_menu(self):
        self.menu = Menu("d")
        self.menu.add_item(MenuItem("Confirm", DeleteAction("user_main")))
        self.menu.add_item(MenuItem("Cancel", SwitchBackAction()))

