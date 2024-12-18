from pydantic import BaseModel


class UserStock(BaseModel):
    stock_id: int = 0
    price: int = 0
    quantity: int = 0
    agency: str = ""
    current_price: int = 0

