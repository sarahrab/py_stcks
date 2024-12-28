import logging
import os
from datetime import datetime

#import logger
from basics import MenuAction
from ViewManager import ViewManager, Model, Transaction, BuyTransaction, SellTransaction
from exceptions.AttemptsException import AttemptsException
from exceptions.StockMarketException import StockMarketException
from exceptions.ValidationException import ValidationException
from logger import StocksAppLogger
from sql_utils.executer import login, get_history, register_user

from stocks import Stock, Stocks
from users import UserAccount, user_mapper
from typing import TypeVar

from validation import TransactionValidation

T = TypeVar("T")

log = logging.getLogger("my_module")
errlog = logging.getLogger("error_log")

class SwitchViewAction(MenuAction):
    def __init__(self, name: str, data: T | None = None):
        super().__init__(data)
        self.name = name

    def execute(self):
        log.debug(f"switch to {self.name}")
        errlog.error("ERROR!!! !!! !!!")
        self.result = ViewManager.switch_view(self.name, self.data)


class SwitchBackAction(MenuAction):
    def __init__(self, data: T | None = None):
        super().__init__(data)
        self.name = "back"

    def execute(self):
        self.result = ViewManager.switch_back(self.data)


class ExitViewAction(MenuAction):
    def __init__(self, data: T | None = None):
        super().__init__(data)

    def execute(self):
        exit(0)


class LoginAction(MenuAction):
    def __init__(self, view_name, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name



    def execute(self):
        StocksAppLogger.debug(f"{__class__.__name__}: Start logging-in...")
        if self.data is None:
            print("Invalid user data")
            ViewManager.switch_view("login", self.result)

        self.result = None
        try:
            self.login_user()
            Model().save_users()
            ViewManager.switch_view(self.view_name, self.result)

        except StockMarketException as e:
            retry = input(e.message)
            if retry.lower() == "y":
                ViewManager.switch_view("login", self.result)
            else:
                ViewManager.switch_back()

    def login_user(self):
        user = Model().users.find(self.data.name, self.data.password)
        if user is not None:
            user.logged_in = True
            self.result = user
        else:
            raise StockMarketException("unknown_user")

class LoginAction1(MenuAction):
    def __init__(self, view_name, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        StocksAppLogger.debug(f"{__class__.__name__}: Start logging-in...")

        if self.data is None:
            print("Invalid user data")
            ViewManager.switch_view("login", self.result)

        self.result = None
        try:
            result = login(self.data.name, self.data.password)
            if result.error == 0 and result.payload is not None:
                u = result.payload
                self.result = user_mapper(result.payload, [])

                self.result = self.data
                self.result.user_id = u.user_id
                self.result.logged_in = True
                # self.result.level = u.level
                self.result.amount = u.amount
                Model().save_users()
                ViewManager.switch_view(self.view_name, self.result)

        except StockMarketException as e:
            retry = input(e.message)
            if retry.lower() == "y":
                ViewManager.switch_view("login", self.result)
            else:
                ViewManager.switch_back()

class RegisterAction(MenuAction):
    def __init__(self, view_name, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        self.result = False
        if self.data is not None:
            reg_user = self.data
            if self.register(reg_user):
                Model().save_users()
                ViewManager.switch_view(self.view_name, self.result)
            else:
                msg = Model().error_messages.get_error_message("user_exists")
                print(msg.replace("{user_name}", reg_user.name))
                ViewManager.switch_back()

            # reg_user = self.data
            # u = Model().users.find(self.data.name)
            # if u is not None:
            #     msg = Model().error_messages.get_error_message("user_exists")
            #     print(msg.replace("{user_name}", reg_user.name))
            #     ViewManager.switch_back()
            #
            # user = Model().users.add(reg_user.name, reg_user.password, reg_user.amount)
            # user.logged_in = True
            # self.result = user
            # # YamlLoader.serialize_users(Model().users, Model().users_db)
            # Model().save_users()
            # ViewManager.switch_view(self.view_name, self.result)

    def register(self, reg_user: UserAccount) -> bool:
        # u = Model().users.find(reg_user.name)
        # if u is not None:
        #     return False

        db_result = register_user(reg_user)
        if db_result is not None:
            self.result = db_result.payload

        # user = Model().users.add(reg_user.name, reg_user.password, reg_user.amount)
        # user.logged_in = True
        # self.result = user
        return db_result is not None and db_result.payload is not None

class LogoutAction(MenuAction):
    def __init__(self, view_name, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        # user = cast(UserAccount, self.data)
        # if user:
        #     user.logged_in = False
        if self.data:
            self.data.logged_in = False
        # YamlLoader.serialize_users(Model().users, Model().users_db)
        Model().save_users()
        ViewManager.switch_view(self.view_name, self.result)


class StartTransactionAction(MenuAction):
    def __init__(self, view_name: str, is_buying: bool, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name
        self.is_buying = is_buying

    def execute(self):
        if self.data is not None:
            # reg_user = cast(UserAccount, self.data)
            self.result = BuyTransaction() if self.is_buying else SellTransaction()
            self.result.user = self.data
            ViewManager.switch_view(self.view_name, self.result)


class SelectStockAction(MenuAction):
    def __init__(self, view_name: str, stock: Stock, data: Transaction | None = None):
        super().__init__(data)
        self.view_name = view_name
        self.stock = stock

    def execute(self):
        # self.result = cast(Transaction, self.data)
        if self.data:
            self.result = self.data
            self.result.stock = self.stock
            self.result.price = self.stock.price
            ViewManager.switch_view(self.view_name, self.result)


class TransactionExecuteAction(MenuAction):
    def __init__(self, view_name: str, data: Transaction | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        transaction = self.data
        if transaction and transaction.user:

            if not self.check_stock_price(transaction):
                print("Stock price has changed.")
                ViewManager.switch_back()

            # VALIDATE()
            # if not self.validate_transaction():
            #     ViewManager.switch_back()

            transaction.execute()
            self.result = transaction

            self.check_requests()

            ViewManager.switch_view(self.view_name, self.result)

    def check_requests(self) -> None:
        interval = int(os.getenv('CHECK_REQUEST_INTERVAL_HOURS'))
        last = os.getenv('LAST_REQUEST_CHECK')
        need_check = False
        if last == '':
            need_check = True
        else:
            dt = datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
            need_check = (datetime.now() - dt).seconds > interval * 3600

        if need_check:
            # update_old_requests()
            os.putenv('LAST_REQUEST_CHECK', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



    def validate_transaction(self) -> bool:
        try:
            result = TransactionValidation.validate_transaction()
            return result.result

        except ValidationException as ve:
            print(f"Validation failed: http_status = {ve.response.status_code}")
            #ViewManager.switch_back()
            return False

        except AttemptsException as ae:
            print("Attempts failed")
            #ViewManager.switch_back()
            return False

    # if not TransactionValidation.validate_transaction():
        #     print("Invalid transaction")
        #     ViewManager.switch_back()

    def check_stock_price(self, transaction: Transaction) -> bool:
        modified = os.path.getmtime(Model().stocks_db)
        if modified != Model().stock_modified_at:
            Model().initialize_stocks()
            stock = Model().stocks.find(transaction.stock.agency)
            if stock is None:
                return False
            else:
                return stock.price == transaction.price
        else:
            return True

    def execute_buy(self, transaction: Transaction):
        if not Model().stocks.remove(transaction.stock.agency, transaction.count):
            transaction.error_msg = "stock BAD"
            return
        self.finalize_transaction(transaction, transaction.user.stocks, -(transaction.stock.price * transaction.count))
        # transaction.user.stocks.add(Stock(agency = transaction.stock.agency,
        #                                   price = transaction.stock.price,
        #                                   count = transaction.count))
        # transaction.user.amount -= transaction.stock.price * transaction.count
        # transaction.error_msg = "success!!!!"

    def execute_sell(self, transaction: Transaction):
        if not transaction.user.stocks.remove(transaction.stock.agency, transaction.count):
            transaction.error_msg = "stock BAD"
            return
        self.finalize_transaction(transaction, Model().stocks, transaction.stock.price * transaction.count)
        # Model().stocks.add(Stock(agency = transaction.stock.agency,
        #                        price = transaction.stock.price,
        #                        count = transaction.count))
        # transaction.user.amount += transaction.stock.price * transaction.count
        # transaction.error_msg = "success!!!!"

    def finalize_transaction(self, transaction: Transaction, stocks: Stocks, amount: int):
        stocks.add(Stock(agency=transaction.stock.agency,
                         price=transaction.stock.price,
                         count=transaction.count))
        transaction.user.amount += amount
        # if transaction.is_buying:
        #     transaction.user.amount -= amount
        # else:
        #     transaction.user.amount += amount
        transaction.error_msg = "success!!!!"


class CloseTransactionAction(MenuAction):
    def __init__(self, view_name: str, data: Transaction | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        transaction = self.data
        if transaction and transaction.user:
            self.result = transaction.user
            # YamlLoader.serialize_users(Model().users, Model().users_db)
            # YamlLoader.serialize_stocks(Model().stocks, Model().stocks_db)
            Model().save()
            ViewManager.switch_view(self.view_name, self.result)


class DeleteAction(MenuAction):
    def __init__(self, view_name: str, data: UserAccount | None = None):
        super().__init__(data)
        self.view_name = view_name

    def execute(self):
        user = self.data
        if user:
            Model().users.remove(user.name)
            # YamlLoader.serialize_users(Model().users, Model().users_db)
            Model().save_users()
            ViewManager.switch_view("welcome")


class SuperDuperTransaction1:
    transaction: Transaction | None = None
    super: int
    duper: str

    #__init__

# class SuperDuperTransaction2(Transaction):
#     super: int
#     duper: str
#
#     def __int__(self, agency: str, amount: int, price: int):
#         super().__init__(agency=agency,...)
class SuperDuperAction(MenuAction):
    def __int__(self, view_name: str, data: SuperDuperTransaction1 | None = None):
        super().__init__(data)
        self.view_name = view_name



