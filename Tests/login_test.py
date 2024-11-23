from inspect import getsourcefile
from typing import cast

import pytest

import os
import sys

from ViewManager import Model

current_path = os.path.abspath(getsourcefile(lambda: 0))
current_dir = os.path.dirname(current_path)
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]

sys.path.insert(0, parent_dir)

import actions

from exceptions.StockMarketException import StockMarketException
from users import UserAccount

Model().users_db = "D:\\python\\py_stcks\\db\\users.yaml"
Model().initialize_users()

@pytest.mark.parametrize("user, expected", [
    (UserAccount(name="ty", password="hhh", amount=0), True),
    (UserAccount(name="yy", password="hhj", amount=0), False)
])
# @pytest.mark.parametrize("name, expected", [
#     ("ty", True),
#     ("yy", False)
# ])
def test_login(user, expected):
    # Model().users_db = "D:\\python\\py_stcks\\db\\users.yaml"
    # Model().initialize_users()
    #user = UserAccount(name=name, password="hhh", amount=0)
    action = actions.LoginAction("l", user)
    try:
        action.login_user()
        u = cast(UserAccount, action.result)
        res = u is not None and u.name == user.name and u.logged_in
        assert res == expected

    except StockMarketException as ex:
        res = action.result is not None
        assert res == expected



# @pytest.mark.parametrize("input_number, expected_output", [
#     (2, True),
#     (3, False),
#     (4, True),
#     (5, False)
# ])
# def test_is_even(input_number, expected_output):
#     # Test the function with different inputs
#     result = input_number % 2 == 0
#     assert result == expected_output
