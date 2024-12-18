from ViewManager import BuyTransaction
from actions import SwitchViewAction, SwitchBackAction
from basics import *

from Utils.utils import Utils
from exceptions.StockMarketException import StockMarketException


class StockCountView(View):
    def get_name(self) -> str:
        return "sc"

    def __init__(self, menu: Menu = None):
        super().__init__(menu)

    def validate_buy(self, amount: int, user_amount: int) -> bool:
        if amount > user_amount:
            raise StockMarketException("not_enough_money")

        elif amount <= 0:
            raise StockMarketException("amount_is_incorrect")

        else:
            return True

    def show(self):
        self.create_menu()
        transaction = self.data
        if transaction and transaction.user:
            print(f"{transaction.user.name} total amount: {transaction.user.amount}")
            is_buying = True if type(self.data) is BuyTransaction else False
            text = "buying" if is_buying else "selling"
            print(f"{text} : {transaction.stock.agency} for {transaction.stock.price}")
            valid = False
            count = 0
            price = 0
            if is_buying:
                while not valid:
                    # amount = self.get_int("input money sum : ")
                    count = Utils.get_int("input money quantity : ")
                    price = Utils.get_int("input price : ")

                    try:
                        valid = self.validate_buy(count * price, transaction.user.amount)
                    except StockMarketException as ex:
                        print(ex.message)

                #count = int(amount / transaction.stock.price)
                print(f"{text} : {count} {transaction.stock.agency} for {count * price}")
            else:
                count = 0
                while not valid:
                    count = Utils.get_int("input stock count : ")
                    if count <= 0:
                        print("error: not valid count")
                    elif count > transaction.stock.count:
                        print("not enough in possession")
                    else:
                        valid = True
                amount = int(count * transaction.stock.price)
                print(f"{text} : {count} {transaction.stock.agency} for {amount}")
            transaction.count = count
            transaction.price = price

    # def get_int(self, element: str) -> int:
    #     value= input(element)
    #     try:
    #         number = int(value)
    #         return  number
    #     except ValueError:
    #         print("invalid format!")
    #         return  0

    def create_menu(self):
        self.menu = Menu("sc")
        self.menu.add_item(MenuItem("Submit", SwitchViewAction("trans")))
        self.menu.add_item(MenuItem("Cancel", SwitchBackAction()))

