from datetime import datetime
from typing import TypeVar
from pydantic import TypeAdapter
from sqlmodel import Session, select

from db_utils import mssql_engine
from sql_utils.models import DBResult, UserModel, RequestModel, TransactionModel, StockModel


def login(name: str, password: str) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserModel).where(UserModel.user_name == name and UserModel.password == password)
            results = session.exec(st)
            u = results.one_or_none()
            if u is not None:
                print(u)
                u.is_logged_in = True
                session.add(u)
                session.commit()
                session.refresh(u)
                return DBResult(payload=u, error=0)
            else:
                return DBResult(error=1)

    except Exception as ex:
        return DBResult(exception="exept")


def login1(session: Session, name: str, password: str) -> DBResult:
    try:
        st = select(UserModel).where(UserModel.user_name == name and UserModel.password == password)
        results = session.exec(st)
        u = results.one_or_none()
        if u is not None:
            print(u)
            u.is_logged_in = True
            session.add(u)
            session.commit()
            session.refresh(u)
            return DBResult(payload=u.user_id, error=0)
        else:
            return DBResult(error=1)

    except Exception as ex:
        return DBResult(exception="exept")


def logout(user_id: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserModel).where(UserModel.user_id == user_id)
            results = session.exec(st)
            u = results.one_or_none()
            if u is not None:
                print(u)
                u.is_logged_in = False
                session.add(u)
                session.commit()
                session.refresh(u)
                return DBResult(payload=u.user_id, error=0)
            else:
                return DBResult(error=2)

    except Exception as ex:
        return DBResult(exception="exept")


def create_buy_request(user_id: int, stock_id: int, price: int, quantity: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            buy_request = RequestModel(requedt_type=True, user_id=user_id, stock_id=stock_id, price=price,
                                       quantity=quantity, timestamp=datetime.datetime, ttl=5)
            session.add(buy_request)
            session.commit()
            session.refresh(buy_request)
            return DBResult(payload=buy_request.request_id, error=0)

    except Exception as ex:
        return DBResult(exception="buyoof")


# add sell


def find_match(request: RequestModel) -> RequestModel | None:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(RequestModel).where(RequestModel.stock_id == request.stock_id).where(
                RequestModel.request_type != request.request_type).where(
                RequestModel.quantity == request.quantity).where(RequestModel.price == request.price).where(
                RequestModel.user_id != request.user_id).where(RequestModel.status == 0)  # open status(pending)
            results = session.exec(st)
            match = results.one_or_none()
            return match

    except Exception as ex:
        return None


def exec_transaction(buy_request: RequestModel, sell_request: RequestModel) -> TransactionModel | None:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            transaction = TransactionModel(buy_request_id=buy_request.request_id,
                                           sell_request_id=sell_request.request_id, timestamp=datetime.datetime)
            session.add(transaction)
            session.commit()
            session.refresh(transaction)
            return transaction

    except Exception as ex:
        return None


def exec_buy(user_id: int, stock_id: int, price: int, quantity: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            buy_request = create_buy(price, quantity, session, stock_id, user_id)
            if buy_request.request_id > 0:
                sell = find_match(buy_request)
                if sell is not None:
                    transaction = exec_transaction(buy_request, sell)
                    if transaction is not None:
                        buy_request.status = 2
                        sell.status = 2  # finished
                        return DBResult(payload=transaction, error=0)
            return DBResult(payload=buy_request, error=0)

    except Exception as ex:
        return DBResult(exception="buyoof")


def create_buy(price, quantity, session, stock_id, user_id):
    buy_request = RequestModel(requedt_type=True, user_id=user_id, stock_id=stock_id, price=price,
                               quantity=quantity, timestamp=datetime.datetime, ttl=5)
    session.add(buy_request)
    session.commit()
    session.refresh(buy_request)
    return buy_request


def finalize_transaction(tran: TransactionModel) -> DBResult:
    engine = mssql_engine()
    # try:
    with Session(engine) as session:
        # req_buy = select(RequestModel.request_id == tran.buy_request_id)
        # req_sell = select(RequestModel.request_id == tran.sell_request_id)
        # buyer = select(UserModel.user_id == req_buy.user_id)
        # seller = select(UserModel.user_id == req_sell.user_id)
        # stock = select(StockModel.stock_id == req_buy.stock=_id)
        # buyer.amount -= req_buy.price * req_buy..q
        # userstock_buyer add stock
        # userstock_seller add stock (find in userStockModel by user_id stock_id each, update if found else insert )
        print("d")
    return DBResult(payload="success", error=0)


def get_stocks() -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(StockModel)
            results = session.exec(st)
            stocks = results.all()
            return DBResult(error=0, payload=stocks)

    except Exception as ex:
        return DBResult(exception="stocks")


def get_history(user_id: int, from_date: datetime | None, to_date: datetime | None, request_type: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            se = select(RequestModel).where(RequestModel.user_id == user_id)
            if from_date is not None:
                se = se.where(RequestModel.timestamp >= from_date)
            if to_date is not None:
                se = se.where(RequestModel.timestamp <= to_date)
            if request_type == 0:   #buy
                se = se.where(RequestModel.request_type == True)
            elif request_type == 1: # sell
                se = se.where(RequestModel.request_type == False)

            res = session.exec(se)
            if res is not None:
                return DBResult(error=0, payload=res.all())
            else:
                return DBResult(error=1)

    except Exception as ex:
        return DBResult(exception="history")
