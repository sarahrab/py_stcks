import yaml

from ViewManager import Model
from YamlLoader import YamlLoader
from basics import *
from stocks import Stock
from users import UserAccount


class WelcomeView(View):
    def __init__(self, title, menu: Menu = None):
        super().__init__(title, menu)

    def show(self):
        print("Welcome, friend!")
        # st = YamlLoader.deserialize_stocks("D:\\python\\py_stcks\\db\\stocks2.yaml")
        # for x in range(6):
        #     Model.stocks.add(Stock(agency=f"Company {x + 1}", price=x + 2, count=(x + 1) * 20))
        # YamlLoader.serialize_stocks(Model.stocks, "D:\\python\\py_stcks\\db\\stocks2.yaml")

        u = UserAccount(name = "User1", password = "kjkj", amount = 9199)
        d = u.model_dump()
        s = yaml.dump(d)
        print(s)
