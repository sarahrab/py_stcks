import asyncio
from contextlib import asynccontextmanager
from typing import List
from fastapi import APIRouter, Depends, FastAPI, Request, status as http_status
from os import getenv
from dotenv import load_dotenv
from config import settings
from fastapi.datastructures import State
import uvicorn
from Models import Stock, StockModel, UserStock, UserStockModel
from StockModel import StockModelCRUD
from UserModel import UserModelCRUD, User, UserModel
from RequestsCRUD import RequestsCRUD
from backtask import run_background_tasks
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

#load_dotenv()
#settings = Settings()

async def get_user_crud(
       session: AsyncSession = Depends(get_async_session)
) -> UserModelCRUD:
   return UserModelCRUD(session=session)

async def get_stock_crud(
       session: AsyncSession = Depends(get_async_session)
) -> StockModelCRUD:
   return StockModelCRUD(session=session)

async def get_request_crud(
      session: AsyncSession = Depends(get_async_session)) -> RequestsCRUD:
   return RequestsCRUD(session=session)
                           


@asynccontextmanager
async def lifespan(app: FastAPI):
   # on startup
   crud = get_request_crud()
   asyncio.create_task(run_background_tasks(crud))
   yield
   # on shutdown
   print("shutdown")

app = FastAPI(
   title=settings.project_name,
   version=settings.version,
   openapi_url=f"{settings.api_v1_prefix}/openapi.json",
   debug=settings.debug,
   lifespan=lifespan
)

limiter = Limiter(key_func=get_remote_address)
#app.state = State()
app.state.limiter=limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


router = APIRouter()

# print(app.version)

@app.get("/", tags=["status"])
async def health_check():
   return {
       "name": settings.project_name,
       "version": settings.version,
       "description": settings.description
   }


@router.post("/users/register/", response_model=UserModel)
@limiter.limit("5/minute")
async def register_user(request: Request, data: User, users: UserModelCRUD = Depends(get_user_crud)):
    u = await users.create(data=data)
    return u

@router.get("/users/{user_id}/", response_model=UserModel)
async def get_user(user_id: int, users: UserModelCRUD = Depends(get_user_crud)):
   u = await users.get_user(user_id);
   return u

@router.post("/users/login/", response_model=UserModel)
async def login(data: User, users: UserModelCRUD = Depends(get_user_crud)):
   u = await users.find(data=data)
   return u

@router.post("/stocks/create/", response_model=StockModel)
async def create_stock(data: Stock, stocks: StockModelCRUD = Depends(get_stock_crud)):
   s = await stocks.create(data=data)
   return s

@router.get("/stocks/{stock_id}/", response_model=StockModel)
async def get_stock(stock_id: int, stocks: StockModelCRUD = Depends(get_stock_crud)):
   s = await stocks.get(stock_id);
   return s

@router.post("/stocks/add_user_stock/", response_model=UserStockModel)
async def add_user_stock(data: UserStock, stocks: StockModelCRUD = Depends(get_stock_crud)):
   s = await stocks.add_user_stock(user_stock=data)
   return s

@router.get("/stocks/get_user_stocks/{user_id}/", response_model=List[UserStock])
async def get_user_stocks(user_id: int, stocks: StockModelCRUD = Depends(get_stock_crud)):
   result = await stocks.get_user_stocks(user_id=user_id)
   return result


app.include_router(router)

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="127.0.0.1", reload=True)