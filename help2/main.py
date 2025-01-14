from fastapi import APIRouter, Depends, FastAPI
from os import getenv
from dotenv import load_dotenv
from config import settings
import uvicorn
from fastapi import status as http_status
from UserModel import UserModelCRUD, User, UserModel
from db import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession

#load_dotenv()
#settings = Settings()

app = FastAPI(
   title=settings.project_name,
   version=settings.version,
   openapi_url=f"{settings.api_v1_prefix}/openapi.json",
   debug=settings.debug
)

async def get_user_crud(
       session: AsyncSession = Depends(get_async_session)
) -> UserModelCRUD:
   return UserModelCRUD(session=session)



router = APIRouter()

# print(app.version)

@app.get("/", tags=["status"])
async def health_check():
   return {
       "name": settings.project_name,
       "version": settings.version,
       "description": settings.description
   }


@router.post("/register/", response_model=UserModel)
async def register_user(data: User, users: UserModelCRUD = Depends(get_user_crud)):
    u = await users.create(data=data)
    return u

@router.post("/reg_u/", response_model=UserModel)
async def register(data: User):
    u = UserModel(user_name=data.name, password=data.password, amount=200, user_id=81)
    return u

@router.get("/users/{user_id}", response_model=UserModel)
async def get_users(user_id: int):
   return UserModel(user_name="ty", password="ggg", amount=200, user_id=user_id)

app.include_router(router)

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="127.0.0.1", reload=True)