import pytest
import asyncio
from httpx import AsyncClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi.testclient import TestClient
from main import app, get_user_crud
from db import Base, get_async_session  # Update with your actual import
from UserModel import UserModelCRUD  # Import your CRUD class
from Models import UserModel  # Import your models
from config import settings

# Test database (file-based SQLite)

# Create an async engine and session maker for testing
# engine = create_async_engine(settings.db_async_connection_str, echo=True)
# TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

engine = create_async_engine(settings.test_db_async_connection_str, echo=False)
TestSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    """Create and drop tables for the test database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Create tables
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # Drop tables after tests

@pytest.fixture(scope="function")
async def async_session(init_db) -> AsyncSession:
    """Provides a new async session for each test."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Rollback after each test