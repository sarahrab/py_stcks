from typing import List, Optional
from pydantic import BaseModel, TypeAdapter, parse_obj_as
from sqlmodel import Field, SQLModel, select
import sqlmodel.ext.asyncio.session
from fastapi import HTTPException, status as http_status

from Models import Stock, StockModel, UserModel, UserStock, UserStockModel, Request, RequestModel

class RequestModelCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def bulk_create(self, data: List[Request]) -> List[Request]:
        if data is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="No data!"
            )

        requests = []
        for req in data:
            result = None
            if req.request_type:    #buy
                result = await self.exec_buy(req)
            else:
                result = await self.exec_sell(req)

            if result:
                requests.append(result)
        return requests


    async def exec_buy(self, data: Request) -> Request:
        # from py_stcks.executor - find_macth, etc.

        return data


    async def exec_sell(self, data: Request) -> Request:
        # from py_stcks.executor - find_macth, etc.

        return data
