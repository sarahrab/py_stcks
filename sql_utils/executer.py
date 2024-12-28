from datetime import datetime, timedelta
from typing import TypeVar
from pydantic import TypeAdapter
from sqlmodel import Session, select, desc

from db_utils import mssql_engine
from sql_utils.models import DBResult, UserModel, RequestModel, TransactionModel, StockModel, UserStockModel, \
    create_user_stock
from users import UserAccount


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


def register_user(ua: UserAccount) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserModel).where(UserModel.user_name == ua.name, UserModel.password == ua.password)
            user = session.exec(st).one_or_none()
            if user is not None:
                return DBResult(exceptions="already exists")

            um = UserModel(user_name=ua.name, password=ua.password, amount=ua.amount, logged_in=True)
            session.add(um)
            session.commit()
            session.refresh(um)
            ua.user_id = um.user_id
            return DBResult(error=0, payload=ua)

    except Exception as ex:
        return DBResult(exception="register")


def create_buy_request(user_id: int, stock_id: int, price: int, quantity: int, ttl: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            expiration_date = datetime.now()
            if ttl > 0:
                expiration_date = expiration_date + timedelta(days=ttl)
            buy_request = RequestModel(requedt_type=True, user_id=user_id, stock_id=stock_id, price=price,
                                       quantity=quantity, timestamp=datetime, ttl=ttl, expiration_date=expiration_date)
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
                RequestModel.quantity == request.quantity).where(
                RequestModel.user_id != request.user_id).where(RequestModel.status == 0)
            if request.request_type:  # buy
                st = st.where(RequestModel.price <= request.price).order_by(RequestModel.price)
            else:
                st = st.where(RequestModel.price >= request.price).order_by(desc(RequestModel.price))

            results = session.exec(st)
            match = results.one_or_none()
            return match

    except Exception as ex:
        return None


def exec_transaction(buy_request: RequestModel, sell_request: RequestModel, price: int) -> TransactionModel | None:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            buy_request.status = 2
            buy_request.price = price
            session.add(buy_request)

            sell_request.status = 2
            sell_request.price = price
            session.add(sell_request)

            transaction = TransactionModel(buy_request_id=buy_request.request_id,
                                           sell_request_id=sell_request.request_id, timestamp=datetime.now())
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
                    transaction = exec_transaction(buy_request, sell, sell.price)
                    if transaction is not None:
                        # buy_request.status = 2
                        # sell.status = 2  # finished
                        return DBResult(payload=transaction, error=0)
                elif buy_request.ttl == 0:
                    buy_request.status = 1  # canceled
                    session.add(buy_request)
                    session.commit()
                    # writeeeeeeee

            return DBResult(payload=buy_request, error=0)

    except Exception as ex:
        return DBResult(exception="buyoof")


def create_buy(price, quantity, session, stock_id, user_id, ttl: int):
    buy_request = RequestModel(requedt_type=True, user_id=user_id, stock_id=stock_id, price=price,
                               quantity=quantity, timestamp=datetime.now(), ttl=ttl)
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


def update_sell_request(session: Session, req_sell: RequestModel, seller: UserModel):
    stock_sell = find_user_stock(session, req_sell)
    if stock_sell:
        new_quantity = stock_sell.quantity - req_sell.quantity
        if new_quantity > 0:
            stock_sell.quantity = new_quantity
            session.add(stock_sell)
        else:
            session.delete(stock_sell)


def update_buy_request(session: Session, req_buy: RequestModel, buyer: UserModel):
    stock_buy = find_user_stock(session, req_buy)
    if stock_buy and stock_buy.price == req_buy.price:
        stock_buy.quantity = stock_buy.quantity + req_buy.quantity

    else:
        stock_buy = UserStockModel(user_id=req_buy.user_id, stock_id=req_buy.stock_id, quantity=req_buy.quantity,
                                   price=req_buy.price)
    session.add(stock_buy)


def update_user_amount(session: Session, user: UserModel, amount: int):
    user.amount += amount
    session.add(user)


def save_transaction_amounts(session: Session, req_buy: RequestModel, req_sell: RequestModel, buyer: UserModel,
                             seller: UserModel):
    update_sell_request(session, req_sell)
    update_buy_request(session, req_buy)
    update_user_amount(session, seller, req_sell.quantity * req_sell.price)
    update_user_amount(session, buyer, -(req_sell.quantity * req_sell.price))
    session.commit()


def find_user_stock(session: Session, req: RequestModel) -> UserStockModel | None:
    st = select(UserStockModel).where(UserStockModel.user_id == req.user_id).where(
        UserStockModel.stock_id == req.stock_id)
    stock_sell = session.exec(st).one_or_none()
    return stock_sell


def check_fus() -> UserStockModel | None:
    engine = mssql_engine()
    with Session(engine) as session:
        st = select(RequestModel).where(RequestModel.request_id == 1)
        r = session.exec(st).one_or_none()
        return find_user_stock(session, r)


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
            # if request_type == 0:   #buy
            #     se = se.where(RequestModel.request_type == True)
            # elif request_type == 1: # sell
            #     se = se.where(RequestModel.request_type == False)

            res = session.exec(se)
            if res is not None:
                all = res.all()
                return DBResult(error=0, payload=all)
            else:
                return DBResult(error=1)

    except Exception as ex:
        return DBResult(exception="history")


# call before creating sell request
#   if DBResult.payload is None: its ok, he can sell
#   if DBResult.payload is RequestModel: he can't sell because on {request.timestamp} he sold by {request.price}
def check_sell_validity(user_id: int, stock_id: int, price: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            se = select(RequestModel).where(RequestModel.user_id == user_id)
            se = se.where(RequestModel.stock_id == stock_id)
            se = se.where(RequestModel.request_type == 0)
            se = se.where(RequestModel.status == 2)
            se = se.order_by(RequestModel.timestamp.desc())
            req = session.exec(se).one_or_none()
            now = datetime.now()
            if req is not None:
                if req.price < price:
                    delta = now - req.timestamp
                    if delta.days < 1:
                        return DBResult(error=0, payload=req)
            return DBResult(error=0, payload=None)

    except Exception as ex:
        return DBResult(exception="history")


def get_user_stocks(user_id: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserStockModel, StockModel).where(UserStockModel.user_id == user_id).join(StockModel)
            results = session.exec(st)
            u = results.all()
            if u is not None and len(u) > 0:
                stocks = []
                for n in u:
                    stocks.append(create_user_stock(n[0], n[1]))
                return DBResult(error=0, payload=stocks)
            else:
                return DBResult(error=7)

    except Exception as ex:
        return DBResult(exception="get_user_stocks")


def get_user(session: Session, user_id: int) -> UserModel | None:
    st = select(UserModel).where(UserModel.user_id == user_id)
    results = session.exec(st)
    return results.one_or_none()


def update_old_requests() -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(RequestModel).where(RequestModel.status == 0).where(RequestModel.expiration_date < datetime())
            results = session.exec(st).all()
            if results:
                for r in results:
                    r.status = 1
                    session.add(r)
                session.commit()


    except Exception as ex:
        return DBResult(exception="update_old_requests")


def delete_user(user_id: int) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st = select(UserModel).where(UserModel.user_id == user_id)
            user = session.exec(st).one_or_none()
            if user:
                session.delete(user)
                session.commit()

    except Exception as ex:
        return DBResult(exception="delete_user_failed")
