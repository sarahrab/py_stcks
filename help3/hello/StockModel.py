from typing import List, Optional
from pydantic import BaseModel, TypeAdapter, parse_obj_as
from sqlmodel import Field, SQLModel, select
import sqlmodel.ext.asyncio.session
from fastapi import HTTPException, status as http_status

from Models import Stock, StockModel, UserModel, UserStock, UserStockModel


class StockModelCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: Stock) -> StockModel:
        sm = StockModel(agency=data.agency, price=data.price, quantity=data.quantity)
        self.session.add(sm)
        await self.session.commit()
        await self.session.refresh(sm)
        return sm

    async def get(self, stock_id: int) -> StockModel:
        statement = select(StockModel).where(StockModel.stock_id == stock_id)
        results = await self.session.exec(statement=statement)
        model = results.one_or_none()  # type: StockModel | None
        if model is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The stock hasn't been found!"
            )
         return model
    
    async def add_user_stock(self, user_stock: UserStock) -> UserStockModel:
        user = await self.session.exec(statement=select(UserModel).where(UserModel.user_id==user_stock.user_id))
        stock_result = await self.session.exec(statement=select(StockModel).where(StockModel.stock_id == user_stock.stock_id))
        stock = stock_result.one_or_none()
        if user.one_or_none() is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )
        if stock is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The stock hasn't been found!"
            )
        model = UserStockModel(user_id=user_stock.user_id, stock_id=user_stock.stock_id, user_price=user_stock.price, user_quantity=user_stock.quantity)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model


    async def get_user_stocks(self, user_id: int) -> Optional[List[UserStock]]:
        st = select(UserStockModel, StockModel).where(UserStockModel.user_id == user_id).join(StockModel, StockModel.stock_id==UserStockModel.stock_id)
        result = await self.session.exec(st)
        sts = result.all()
        stocks = []
        for s in sts:
            us = UserStock(user_id=s[0].user_id, stock_id=s[0].stock_id, agency=s[1].agency, price=s[0].user_price,
                           quantity=s[0].user_quantity, current_price=s[1].price)
            stocks.append(us)
        return stocks

  # CLIENT: UserStocksView
  def show_stock_diff(us: UserStock):
    paid = us.price * us.quantity
    current_value = us.current_price * us.quantity
    diff = current_value - paid
    print(f"Diff: {diff}, ({diff * 100 / paid}%)")