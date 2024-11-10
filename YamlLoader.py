from typing import Optional

from pydantic import BaseModel
import yaml

from stocks import Stocks
from users import UserAccount, UserManager


class YamlLoader:
    @classmethod
    def serialize_stocks(cls, stocks: Stocks, filename: str):
        if stocks:
            stocks_dict = stocks.model_dump()
            # stocks_yaml = yaml.dump(stocks_dict)
            with open(filename, 'w') as file:
                yaml.dump(stocks_dict, file)

    @classmethod
    def deserialize_stocks(cls, filename: str) -> Stocks | None:
        result: Optional[Stocks] = None
        try:
            with open(filename, 'r') as file:
                stocks_yaml = yaml.safe_load(file)
                result = Stocks(**stocks_yaml)
        except:
            result = None
        finally:
            return result

    @classmethod
    def serialize_users(cls, users: UserManager, filename: str):
        if users:
            users_dict = users.model_dump()
            with open(filename, 'w') as file:
                yaml.dump(users_dict, file)


    @classmethod
    def deserialize_users(cls, filename: str) -> UserManager | None:
        result: Optional[UserManager] = None
        try:
            with open(filename, 'r') as file:
                users_yaml = yaml.safe_load(file)
                result = UserManager(**users_yaml)
        except:
            result = None
        finally:
            return result
