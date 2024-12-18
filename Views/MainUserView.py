from actions import LogoutAction, StartTransactionAction, SwitchViewAction
from basics import *

from users import *

actions_dict= {
    "check_funds": SwitchViewAction("user_funds"),
    "check_stock": SwitchViewAction("user_stocks"),

}
class MainUserView(View):
    def get_name(self) -> str:
        return "user_main"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def show(self):
        self.create_menu()

        user = None
        if type(self.data) == UserAccount:
            user = self.data
        else:
            user = self.data.user

        if user is not None:
            print(f"Hello again, {user.name}!")
            #user.stocks.add(Stock(agency = "nayax", price = 25, count = 10))  # test only
            #YamlLoader.serialize_users(Model.users, "D:\\python\\py_stcks\\db\\users.yaml")

    def create_menu(self):
        self.menu = Menu("u")

        # load user_actions.yaml
        # foreach user_action_def from yaml:
        #   get action from actions_dict
        #   if user_action_def.contain(self.data.level):
        #       self.menu.add_item(user_action_def.action_caption, action[user_action_def.action_key])

        # a = ActionsModel()
        # a.initialize("D:\\python\\py_stcks\\db\\e1.yaml")
        # actions = a.get_actions(self.data.level)
        # for act in actions:
        #     f = actions_dict[act.action_key]
        #     self.menu.add_item(MenuItem(act.action_caption, f))

        self.menu.add_item(MenuItem("Check Funds", SwitchViewAction("user_funds")))
        self.menu.add_item(MenuItem("Check Stock", SwitchViewAction("user_stocks")))
        self.menu.add_item(MenuItem("Buy", StartTransactionAction("buy", True)))
        self.menu.add_item(MenuItem("Sell", StartTransactionAction("sell", False)))
        self.menu.add_item(MenuItem("Logout", LogoutAction("welcome")))
        self.menu.add_item(MenuItem("Delete Account", SwitchViewAction("delete")))
        # if self.data.level == 0:
            # self.menu.add_item( "Add stock")


