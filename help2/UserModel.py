from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from sqlmodel import Field, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

class User(BaseModel):
    name: str
    password: str
    amount: float
    
class UserModel(SQLModel, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    user_name: str
    password: str
    is_logged_id: Optional[bool] = None
    is_deleting: Optional[bool] = None
    amount: float
    login_updated: Optional[datetime] = None


class UserModelCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: User) -> UserModel:
        um = UserModel(user_name=data.name, password=data.password, amount=data.amount)
        self.session.add(um)
        await self.session.commit()
        await self.session.refresh
        return um

