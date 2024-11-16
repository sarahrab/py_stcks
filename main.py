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
from basics import MenuItem, Menu
from actions import *
from dotenv import load_dotenv
import os

from validation import TransactionValidation


def init_views():

    # menu_welcome = Menu("w")
    # menu_welcome.add_item(MenuItem("1", "Login", SwitchViewAction("login")))
    # menu_welcome.add_item(MenuItem("2", "Register", SwitchViewAction("regUser")))
    # menu_welcome.add_item(MenuItem("3", "Exit", ExitViewAction()))
    #welcomeView = WelcomeView("welcome", menu_welcome)
    welcomeView = WelcomeView("welcome")
    ViewManager.add_view(welcomeView)

    # menu_login = Menu("l")
    # menu_login.add_item(MenuItem("1", "Submit", LoginAction("user_main")))
    # menu_login.add_item(MenuItem("2", "Cancel", SwitchViewAction("welcome")))
    #loginView = LoginView("login", menu_login)
    loginView = LoginView("login")
    ViewManager.add_view(loginView)

    # menu_reg = Menu("r")
    # menu_reg.add_item(MenuItem("1", "Submit", RegisterAction("user_main")))
    # menu_reg.add_item(MenuItem("2", "Cancel", SwitchViewAction("welcome")))
    #regUserView = RegisterUserView("regUser", menu_reg)
    regUserView = RegisterUserView("regUser")
    ViewManager.add_view(regUserView)

    # menu_user = Menu("u")
    # menu_user.add_item(MenuItem("1", "Check Funds", SwitchViewAction("user_funds")))
    # menu_user.add_item(MenuItem("2", "Check Stock", SwitchViewAction("user_stocks")))
    # menu_user.add_item(MenuItem("3", "Buy", StartTransactionAction("buy", True)))
    # menu_user.add_item(MenuItem("4", "Sell", StartTransactionAction("sell", False)))
    # menu_user.add_item(MenuItem("5", "Logout", LogoutAction("welcome")))
    #userView = MainUserView("user_main", menu_user)
    userView = MainUserView("user_main")
    ViewManager.add_view(userView)

    # menu_funds = Menu("f")
    # menu_funds.add_item(MenuItem("1", "Back", SwitchBackAction()))

    #userFundsView = UserFundsView("user_funds", menu_funds)
    userFundsView = UserFundsView("user_funds")
    ViewManager.add_view(userFundsView)
    #userStocksView = UserStocksView("user_stocks", menu_funds)
    userStocksView = UserStocksView("user_stocks")
    ViewManager.add_view(userStocksView)

    buyingView = BuyingView("buy")
    ViewManager.add_view(buyingView)

    sellingView = SellingView("sell")
    ViewManager.add_view(sellingView)

    # menu_count = Menu("sc")
    # menu_count.add_item(MenuItem("1", "Submit", SwitchViewAction("trans")))
    # menu_count.add_item(MenuItem("2", "Cancel", SwitchBackAction()))
    #sc = StockCountView("sc", menu_count)
    sc = StockCountView("sc")
    ViewManager.add_view(sc)

    # menu_trans = Menu("tr")
    # menu_trans.add_item(MenuItem("1", "Submit", TransactionExecuteAction("result")))
    # menu_trans.add_item(MenuItem("2", "Cancel", SwitchBackAction()))
    # trans_view = TransactionSummaryView("trans", menu_trans)
    trans_view = TransactionSummaryView("trans")
    ViewManager.add_view(trans_view)

    # menu_result = Menu("r")
    # menu_result.add_item(MenuItem("1", "Continue", CloseTransactionAction("user_main")))
    # result_view = TransactionResultView("result", menu_result)
    result_view = TransactionResultView("result")
    ViewManager.add_view(result_view)

    delete_view = DeleteView("delete")
    ViewManager.add_view(delete_view)


if __name__ == '__main__':

    # Model.stocks = YamlLoader.deserialize_stocks(Model.stocks_db)
    # Model.users = YamlLoader.deserialize_users(Model.users_db)

    load_dotenv()
    Model().users_db = os.getenv('USERS_DB_FILE')
    Model().stocks_db = os.getenv('STOCKS_DB_FILE')
    Model().error_messages_db = os.getenv('DB_ERRORS')
    Model().initialize()

    TransactionValidation.validation_url = os.getenv('VALIDATION_ENDPOINT')

    init_views()
    ViewManager.switch_view("welcome")
