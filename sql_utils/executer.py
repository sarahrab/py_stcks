from pydantic import TypeAdapter
from sqlmodel import Session, select

from db_utils import mssql_engine
from sql_utils.models import DBResult, UserModel


def login(name: str, password: str) -> DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st= select(UserModel).where(UserModel.user_name == name and UserModel.password== password)
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

def login1(session: Session, name: str, password: str) -> DBResult:
    try:
        st= select(UserModel).where(UserModel.user_name == name and UserModel.password== password)
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


def logout(user_id: int) ->DBResult:
    engine = mssql_engine()
    try:
        with Session(engine) as session:
            st= select(UserModel).where(UserModel.user_id == user_id)
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

