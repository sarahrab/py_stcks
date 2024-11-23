from basics import *
from pydantic import BaseModel
from typing import List, Dict


class Stock(BaseModel):
    agency: str
    price: int
    count: int

    # def __init__(self, agency, price, count):
    #     self.agency = agency
    #     self.price = price
    #     self.count = count

    def get_cost(self) -> int:
        return self.price * self.count

    def to_string(self) -> str:
        return f"{self.agency}, Price: {self.price}, Amount: {self.count}, Total: {self.get_cost()}"

    def to_item(self, id: str) -> MenuItem:
        return MenuItem(id, self.to_string(), None)


class Stocks(BaseModel):
    #stocks: List[Stock] = []
    stocks: Dict[str, Stock] = {}

    # def __init__(self):
    #     self.stocks = []

    def add(self, stock: Stock):
        # old = self.find(stock.agency)
        # if old is not None:
        #     old.price = stock.price
        #     old.count += stock.count
        # else:
        #     self.stocks.append(stock)
        if not self.stocks.__contains__(stock.agency):
            self.stocks[stock.agency] = stock
        else:
            self.stocks[stock.agency].price = stock.price
            self.stocks[stock.agency].count += stock.count

    def find(self, agency: str) -> Stock | None:
        # for stock in self.stocks:
        #     if stock.agency == agency:
        #         return stock
        if self.stocks.__contains__(agency):
            return self.stocks[agency]
        return None

    def get_stocks_value(self) -> int:
        # total = 0
        # for stock in self.stocks:
        #     total += stock.get_cost()
        # return total
        return sum([stock.get_cost() for stock in self.stocks])

    def remove(self, agency: str, count: int) -> bool:
        stock = self.find(agency)
        if stock:
            stock.count -= count
            if stock.count <= 0:
                self.stocks.remove(stock)
            return True
        return False

    def count(self):
        return len(self.stocks)