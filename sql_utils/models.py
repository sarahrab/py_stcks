from datetime import datetime
from typing import Optional, TypeVar, List

from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field

from sql_utils.user_stock import UserStock

T = TypeVar("T")


class StockModel(SQLModel, table=True):
    __tablename__ = "TBL_STOCKS"
    stock_id: Optional[int] = Field(default=None, primary_key=True)
    agency: str
    price: int
    quantity: int


def stock_to_string(stock: StockModel) -> str:
    return f"{stock.agency}, Price: {stock.price}, Amount: {stock.quantity}, Total: {stock.price * stock.quantity}"


class UserStockModel(SQLModel, table=True):
    __tablename__ = "TBL_USER_STOCKS"
    user_stock_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="TBL_USERS.user_id")
    stock_id: int = Field(foreign_key="TBL_STOCKS.stock_id")
    price: int
    quantity: int


class UserModel(SQLModel, table=True):
    __tablename__ = "TBL_USERS"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str | None
    password: int | None
    amount: int | None
    is_logged_in: bool | None = Field(default=False)
    level: Optional[int] = 0


def create_user_stock(usm: UserStockModel, sm: StockModel) -> UserStock:
    return UserStock(stock_id=usm.stock_id, price=usm.price, quantity=usm.quantity, agency=sm.agency,
                     current_price=sm.price)


class RequestModel(SQLModel, table=True):
    __tablename__ = "TBL_REQUESTS"
    request_id: Optional[int] = Field(default=None, primary_key=True)
    request_type: Optional[bool]
    user_id: Optional[int] = Field(default=None)
    stock_id: Optional[int] = Field(default=None)
    quantity: int | None
    price: int | None
    status: int | None
    timestamp: datetime | None
    ttl: int | None


class TransactionModel(SQLModel, table=True):
    __tablename__ = "TBL_TRANSACTIONS"
    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    buy_request_id: Optional[int] = Field(default=None)
    sell_request_id: Optional[int] = Field(default=None)
    timestamp: datetime | None


class DBResult(BaseModel):
    payload: T | None = None
    error: int = 0
    exception: str = ''
