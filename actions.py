from basics import MenuAction
from ViewManager import ViewManager, Model, Transaction
from typing import cast

from stocks import Stock
from users import UserAccount, User


class SwitchViewAction(MenuAction):
    def __init__(self, name: str, data: object | None = None):
        super().__init__(data)
        self.name = name

    def execute(self):
        self.result = ViewManager.switch_view(self.name, self.data)


class SwitchBackAction(MenuAction):
    def __init__(self, data: object | None = None):
        super().__init__(data)
        self.name = "back"

    def execute(self):
        self.result = ViewManager.switch_back(self.data)


class ExitViewAction(MenuAction):
    def __init__(self, data: object | None = None):
        super().__init__(data)

    def execute(self):
        exit(0)


class LoginAction(MenuAction):
    def __init__(self, view_name, data: object | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        self.result = False
        find = cast(User, self.data)
        if find is not None:
            user = Model.users.find(find.name, find.password)
            if user is not None:
                user.logged_in = True
                self.result = user
                ViewManager.switch_view(self.view_name, self.result)
            else:
                print("Unknown user. Please try again.")
                ViewManager.switch_view("login", self.result)


class RegisterAction(MenuAction):
    def __init__(self, view_name, data: object | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        self.result = False
        if self.data is not None:
            reg_user = cast(UserAccount, self.data)
            user = Model.users.add(reg_user.name, reg_user.password, reg_user.amount)
            user.logged_in = True
            self.result = user
            ViewManager.switch_view(self.view_name, self.result)


class StartTransactionAction(MenuAction):
    def __init__(self, view_name: str, is_buying: bool, data: object | None = None):
        super().__init__(data)
        self.view_name = view_name
        self.is_buying = is_buying

    def execute(self):
        if self.data is not None:
            reg_user = cast(UserAccount, self.data)
            self.result = Transaction(self.is_buying)
            self.result.user = reg_user
            ViewManager.switch_view(self.view_name, self.result)


class SelectStockAction(MenuAction):
    def __init__(self, view_name: str, stock: Stock, data: object | None = None):
        super().__init__(data)
        self.view_name = view_name
        self.stock = stock

    def execute(self):
        self.result = cast(Transaction, self.data)
        if self.result:
            self.result.stock = self.stock
            ViewManager.switch_view(self.view_name, self.result)


class TransactionExecuteAction(MenuAction):
    def __init__(self, view_name: str, data: object | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        transaction = cast(Transaction, self.data)
        if transaction and transaction.user:
            if transaction.is_buying:
                self.execute_buy(transaction)
            else:
                self.execute_sell(transaction)
            ViewManager.switch_view(self.view_name, self.result)

    def execute_buy(self, transaction: Transaction):
        if not Model.stocks.remove(transaction.stock.agency, transaction.count):
            transaction.error_msg = "stock BAD"
            return
        transaction.user.stocks.add(Stock(transaction.stock.agency, transaction.stock.price, transaction.count))
        transaction.user.amount -= transaction.stock.price * transaction.count
        transaction.error_msg = "success!!!!"

    def execute_sell(self, transaction: Transaction):
        if not transaction.user.stocks.remove(transaction.stock.agency, transaction.count):
            transaction.error_msg = "stock BAD"
            return
        Model.stocks.add(Stock(transaction.stock.agency, transaction.stock.price, transaction.count))
        transaction.user.amount += transaction.stock.price * transaction.count
        transaction.error_msg = "success!!!!"
