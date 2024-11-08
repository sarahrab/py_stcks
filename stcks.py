from basics import *


class Stock:
    def __init__(self, agency, price, count):
        self.agency = agency
        self.price = price
        self.count = count

    def get_cost(self) -> int:
        return self.price * self.count

    def to_string(self) -> str:
        return f"{self.agency}, Price: {self.price}, Amount: {self.count}, Total: {self.get_cost()}"

    def to_item(self, id: str) -> MenuItem:
        return MenuItem(id, self.to_string(), None)


class Stocks:
    def __init__(self):
        self.stocks = []

    def add(self, stock):
        old = self.find(stock.agency)
        if old is not None:
            old.price = stock.price
            old.count += stock.count
        else:
            self.stocks.append(stock)

    def find(self, agency: str) -> Stock | None:
        for stock in self.stocks:
            if stock.agency == agency:
                return stock
        return None

    def get_stocks_value(self) -> int:
        total = 0
        for stock in self.stocks:
            total += stock.get_cost()
        return total

    def make_menu(self) -> Menu:
        id = 1
        menu = Menu("stocks")
        for stock in self.stocks:
            item = stock.to_item(id)
            menu.add_item(item)
            id = id + 1
        return menu
