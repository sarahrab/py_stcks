from ViewManager import ViewManager, Model
from Views.LoginView import LoginView, RegisterUserView
from Views.UserFundsView import UserFundsView
from Views.UserStocksView import UserStocksView
from Views.WelcomeView import WelcomeView
from Views.MainUserView import MainUserView
from Views.BuyingView import BuyingView
from Views.SellingView import SellingView
from Views.TransactionView import TransactionView
from basics import MenuItem, Menu
from actions import *


def init_views():
    menu_welcome = Menu("w")
    menu_welcome.add_item(MenuItem("1", "Login", SwitchViewAction("login")))
    menu_welcome.add_item(MenuItem("2", "Register", SwitchViewAction("regUser")))
    menu_welcome.add_item(MenuItem("3", "Exit", ExitViewAction()))
    welcomeView = WelcomeView("welcome", menu_welcome)
    ViewManager.add_view(welcomeView)

    menu_login = Menu("l")
    menu_login.add_item(MenuItem("1", "Submit", LoginAction("user_main")))
    menu_login.add_item(MenuItem("2", "Cancel", SwitchViewAction("welcome")))
    loginView = LoginView("login", menu_login)
    ViewManager.add_view(loginView)

    menu_reg = Menu("r")
    menu_reg.add_item(MenuItem("1", "Submit", RegisterAction("user_main")))
    menu_reg.add_item(MenuItem("2", "Cancel", SwitchViewAction("welcome")))
    regUserView = RegisterUserView("regUser", menu_reg)
    ViewManager.add_view(regUserView)

    menu_user = Menu("u")
    menu_user.add_item(MenuItem("1", "Check Funds", SwitchViewAction("user_funds")))
    menu_user.add_item(MenuItem("2", "Check Stock", SwitchViewAction("user_stocks")))
    menu_user.add_item(MenuItem("3", "Buy", SwitchViewAction("buy")))
    menu_user.add_item(MenuItem("4", "Sell", SwitchViewAction("sell")))
    menu_user.add_item(MenuItem("5", "Logout", SwitchViewAction("welcome")))
    userView = MainUserView("user_main", menu_user)
    ViewManager.add_view(userView)

    menu_funds = Menu("f")
    menu_funds.add_item(MenuItem("1", "Back", SwitchViewAction("user_main")))

    userFundsView = UserFundsView("user_funds", menu_funds)
    ViewManager.add_view(userFundsView)
    userStocksView = UserStocksView("user_stocks", menu_funds)
    ViewManager.add_view(userStocksView)

    menu_buy= Model.stocks.make_menu()
    menu_buy.add_item(MenuItem(f"{menu_buy.count() + 1}", "Back", SwitchViewAction("user_main")))
    buyingView= BuyingView("buy", menu_buy)
    ViewManager.add_view(buyingView)

    trans_view= TransactionView

if __name__ == '__main__':
    init_views()
    ViewManager.switch_view("welcome")
