from typing import List, Optional
from pydantic import BaseModel, TypeAdapter, parse_obj_as
from sqlmodel import Field, SQLModel, select, desc
import sqlmodel.ext.asyncio.session
from fastapi import HTTPException, status as http_status
import datetime

from Models import Stock, StockModel, UserModel, UserStock, UserStockModel, Request, RequestModel, TransactionModel, \
    create_request_model


class RequestModelCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def execute(self, data: Request) -> Request:
        if data is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="No data!"
            )

        result = None
        if data.request_type:  # buy
            result = await self.exec_buy(data)
        else:
            result = await self.exec_sell(data)
        return result


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
        match = await self.find_match(request=data)
        if match:
            buy_request = create_request_model(data)
            transaction = await self.exec_transaction(buy_request=buy_request, sell_request=match, price=match.price)
            if transaction is not None:
                # buy_request.status = 2
                # sell.status = 2  # finished

        elif match.ttl == 0:
            data.status = 1  # canceled
            self.session.add(data)
            self.session.commit()

        return data


    async def exec_sell(self, data: Request) -> Request:
        # from py_stcks.executor - find_macth, etc.

        return data

    async def find_match(self, request: Request) -> RequestModel | None:
        try:
            st = select(RequestModel).where(RequestModel.stock_id == request.stock_id).where(
                RequestModel.request_type != request.request_type).where(
                RequestModel.quantity == request.quantity).where(
                RequestModel.user_id != request.user_id).where(RequestModel.status == 0).where(
                    RequestModel.expiration_date >= datetime.datetime.now())
            if request.request_type:  # buy
                st = st.where(RequestModel.price <= request.price).order_by(RequestModel.price)
            else:
                st = st.where(RequestModel.price >= request.price).order_by(desc(RequestModel.price))

            results = await self.session.exec(st)
            match = results.one_or_none()
            return match

        except Exception as ex:
            return None

    async def exec_transaction(buy_request: RequestModel, sell_request: RequestModel, price: int) -> TransactionModel | None:
        try:
            buy_request.status = 2
            buy_request.price = price
            await self.session.add(buy_request)

            sell_request.status = 2
            sell_request.price = price
            self.session.add(sell_request)

            transaction = TransactionModel(buy_request_id=buy_request.request_id,
                                           sell_request_id=sell_request.request_id, timestamp=datetime.datetime.now())
            session.add(transaction)

            session.commit()

            session.refresh(transaction)
            return transaction

        except Exception as ex:
            return None
