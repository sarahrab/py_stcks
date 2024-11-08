from ViewManager import Model
from basics import *
from stocks import Stock


class WelcomeView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        print("Welcome, friend!")
        for x in range(6):
            Model.stocks.add(Stock(f"Company {x + 1}", x + 2, (x + 1) * 20))




