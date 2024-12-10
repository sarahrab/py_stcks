from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel
from sqlalchemy import DateTime
from sqlmodel import SQLModel, Field


# T = TypeVar("T")


# class StockModel(SQLModel, table=True):
#     __tablename__ = "TBL_STOCKS"
#     stock_id: Optional[int] = Field(default=None, primary_key=True)
#     agency: str
#     price: int
#     quantity: int
#

class UserModel(SQLModel, table=True):
    __tablename__ = "TBL_USERS"
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str | None
    password: int | None
    amount: int | None
    is_logged_in: bool | None = Field(default=False)


# class UserStockModel(SQLModel, table=True):
#     __tablename__ = "TBL_USER_STOCKS"
#     user_stock_id: Optional[int] = Field(default=None, primary_key=True)
#     user_id: int
#     stock_id: int
#     price: int
#     quantity: int

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
    payload: object | None = None
    error: int = 0
    exception: str = ''
