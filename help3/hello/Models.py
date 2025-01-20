from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class User(BaseModel):
    name: str
    password: str
    amount: float
    
class UserModel(SQLModel, table=True):
    __tablename__ = "TBL_USERS"

    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    password: str
    is_logged_id: Optional[bool] = None
    is_deleting: Optional[bool] = None
    amount: float
    login_updated: Optional[datetime] = None

class Stock(BaseModel):
    agency: str
    price: float
    quantity: int


class StockModel(SQLModel, table=True):
    __tablename__="TBL_STOCKS"

    stock_id: Optional[int] = Field(default=None, primary_key=True)
    agency: Optional[str] = Field(default=None, nullable=False)
    price: Optional[float] = Field(default=0, decimal_places=3)
    quantity: Optional[int] = Field(default=0)


class UserStockModel(SQLModel, table=True):
    __tablename__="TBL_USER_STOCKS"

    user_stock_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, nullable=False)
    stock_id: Optional[int] = Field(default=None, nullable=False)
    user_price: Optional[float] = Field(default=0, decimal_places=3)
    user_quantity: Optional[int] = Field(default=0)


class UserStock(BaseModel):
    user_id: int
    stock_id: int
    agency: str
    price: float
    quantity: int
    current_price: float


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
    expiration_date: datetime | None

class Request(BaseModel):
    request_type: bool
    user_id: int
    stock_id: int
    quantity: int
    price: float
    ttl: int
    status: int | None


def create_request_model(request: Request) -> RequestModel:
    return RequestModel(request_type=request.request_type, user_id=request.user_id, stock_id=request.stock_id,
                        quantity=request.quantity, price=request.price, status=1, ttl=request.ttl)
class TransactionModel(SQLModel, table=True):
    __tablename__ = "TBL_TRANSACTIONS"

    transaction_id: Optional[int] = Field(default=None, primary_key=True)
    buy_request_id: Optional[int] = Field(default=None)
    sell_request_id: Optional[int] = Field(default=None)
    timestamp: datetime | None


