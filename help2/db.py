from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
import aiosqlite

async_engine = create_async_engine(
   settings.db_async_connection_str,
   echo=True,
   future=True
)


async def get_async_session() -> AsyncSession:
   async_session = sessionmaker(
       bind=async_engine, class_=AsyncSession, expire_on_commit=False
   )
   async with async_session() as session:
       yield session