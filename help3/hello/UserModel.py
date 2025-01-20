from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status as http_status
from pydantic import BaseModel
from sqlmodel import Field, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from Models import User, UserModel


class UserModelCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: User) -> UserModel:
        um = UserModel(user_name=data.name, password=data.password, amount=data.amount)
        self.session.add(um)
        await self.session.commit()
        await self.session.refresh(um)
        return um

    async def find(self, data: User) -> UserModel:
        statement = select(UserModel).where(UserModel.user_name == data.name).where(UserModel.password == data.password)
        results = await self.session.exec(statement=statement)
        model = results.one_or_none()  # type: UserModel | None
        if model is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )
        return model
    
    async def get_user(self, user_id: int) -> UserModel:
        statement = select(UserModel).where(UserModel.user_id == user_id)
        results = await self.session.exec(statement=statement)
        model = results.one_or_none()  # type: UserModel | None
        if model is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )
        return model