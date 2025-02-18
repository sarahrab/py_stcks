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

class Request(BaseModel):
    request_id: int
    request_type: bool
    user_id: int
    stock_id: int
    price: float
    quantity: int
    ttl: int

class RequestModel(SQLModel, table=True):
    __tablename__="TBL_REQUESTS"

    request_id: Optional[int] = Field(default=None, primary_key=True)
    request_type: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None, nullable=False)
    stock_id: Optional[int] = Field(default=None, nullable=False)
    price: Optional[float] = Field(default=0, decimal_places=3)
    quantity: Optional[int] = Field(default=0)
    status: Optional[int] = Field(default=0)
    ttl: Optional[int] = Field(default=0)
    expiration_date: datetime = Field(default=None)


