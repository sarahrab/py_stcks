import atexit
import configparser
import json
import logging
import pathlib

from basics import View
from actions import *
from dotenv import load_dotenv
import os
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
from db_utils import mssql_engine
from logger import StocksAppLogger
from sql_utils.models import StockModel
from user_actions import ActionsModel
from validation import TransactionValidation
from sql_utils.executer import login, logout, get_user_stocks, update_old_requests, check_fus
import logging.config
import logging.handlers



def init_views():
    views = ["welcome", "login", "regUser", "user_main", "user_funds", "user_stocks", "buy", "sell", "sc", "result", "trans", "delete"]
    for view in views:
        V = View(view)
        ViewManager.add_view(V)

def setup_logger():
    path = pathlib.Path("logger.json")
    with open(path) as f:
        config = json.load(f)
    logging.config.dictConfig(config)
    queue_handler = logging.getHandlerByName("queue_handler")
    if queue_handler:
        queue_handler.listener.start()
        atexit.register(queue_handler.listener.stop)

def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read('config.ini')

    # Access values from the configuration file
    max_validation_attempts = config.getint('General', 'MAX_VALIDATION_ATTEMPTS')
    interval = config.getint('General', 'CHECK_REQUEST_INTERVAL_HOURS')
    # config.has_option()
    # config.has_section()

    # Return a dictionary with the retrieved values



if __name__ == '__main__':

    # a = ActionsModel()
    # a.initialize("D:\\python\\py_stcks\\db\\e1.yaml")
    # l = a.get_actions(1)

#    update_old_requests()
    us = check_fus()

    f = get_user_stocks(1)
    if f.payload:
        for sm in f.payload:
            print(f"Stock={sm.agency}, quantity={sm.quantity}, paid price={sm.price}, current price ={sm.current_price}, "
                  f"profit={sm.quantity * sm.current_price - sm.quantity * sm.price}")

    # Model.stocks = YamlLoader.deserialize_stocks(Model.stocks_db)
    # Model.users = YamlLoader.deserialize_users(Model.users_db)

    login = login("ty", "hhh")
    logout = logout(1)
    load_dotenv()

    dir = os.getcwd()

    # logging.basicConfig(filename='stocks.log')
    # logger = logging.getLogger(__name__)
    # logger.setLevel(logging.DEBUG)
    StocksAppLogger.initialize()
    StocksAppLogger.debug("Starting")

    Model().users_db = os.getenv('USERS_DB_FILE')
    if not os.path.exists(Model().users_db):
        Model().users_db = os.path.join(dir, "users.yaml")

    Model().stocks_db = os.getenv('STOCKS_DB_FILE')
    Model().error_messages_db = os.getenv('DB_ERRORS')
    Model().initialize()
    StocksAppLogger.debug(f"Model initialized: {len(Model().users.users)} users, {len(Model().stocks.stocks)} stocks")

    TransactionValidation.validation_url = os.getenv('VALIDATION_ENDPOINT')
    TransactionValidation.max_tries = os.getenv('MAX_VALIDATION_ATTEMPTS')

    init_views()
    StocksAppLogger.debug("views initialized")

    ViewManager.switch_view("welcome")
