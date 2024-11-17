from ViewManager import ViewManager, Model
from Views.DeleteView import DeleteView
from Views.LoginView import LoginView
from Views.RegisterUserView import RegisterUserView
from Views.StockCountView import StockCountView
from Views.TransactionResultVIew import TransactionResultView
from Views.UserFundsView import UserFundsView
from Views.UserStocksView import UserStocksView
from Views.WelcomeView import WelcomeView
from Views.MainUserView import MainUserView
from Views.BuyingView import BuyingView
from Views.SellingView import SellingView
from Views.TransactionSummaryView import TransactionSummaryView
from YamlLoader import YamlLoader
from basics import MenuItem, Menu, View
from actions import *
from dotenv import load_dotenv
import os

from validation import TransactionValidation


def init_views():

    views = ["welcome", "login", "regUser", "user_main", "user_funds", "user_stocks", "buy", "sell", "sc", "result", "trans", "delete"]
    for view in views:
        ViewManager.add_view(View(view))

    # welcomeView = WelcomeView("welcome")
    # ViewManager.add_view(welcomeView)
    #
    # loginView = LoginView("login")
    # ViewManager.add_view(loginView)
    #
    # regUserView = RegisterUserView("regUser")
    # ViewManager.add_view(regUserView)
    #
    # userView = MainUserView("user_main")
    # ViewManager.add_view(userView)
    #
    # userFundsView = UserFundsView("user_funds")
    # ViewManager.add_view(userFundsView)
    # userStocksView = UserStocksView("user_stocks")
    # ViewManager.add_view(userStocksView)
    #
    # buyingView = BuyingView("buy")
    # ViewManager.add_view(buyingView)
    #
    # sellingView = SellingView("sell")
    # ViewManager.add_view(sellingView)
    #
    # sc = StockCountView("sc")
    # ViewManager.add_view(sc)
    #
    # trans_view = TransactionSummaryView("trans")
    # ViewManager.add_view(trans_view)
    #
    # result_view = TransactionResultView("result")
    # ViewManager.add_view(result_view)
    #
    # delete_view = DeleteView("delete")
    # ViewManager.add_view(delete_view)


if __name__ == '__main__':

    # Model.stocks = YamlLoader.deserialize_stocks(Model.stocks_db)
    # Model.users = YamlLoader.deserialize_users(Model.users_db)

    load_dotenv()

    dir = os.getcwd()

    Model().users_db = os.getenv('USERS_DB_FILE')
    if not os.path.exists(Model().users_db):
        Model().users_db = os.path.join(dir, "users.yaml")

    Model().stocks_db = os.getenv('STOCKS_DB_FILE')
    Model().error_messages_db = os.getenv('DB_ERRORS')
    Model().initialize()

    TransactionValidation.validation_url = os.getenv('VALIDATION_ENDPOINT')

    init_views()
    ViewManager.switch_view("welcome")
