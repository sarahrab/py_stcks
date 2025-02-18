import pytest
from httpx import AsyncClient
import pytest_asyncio
from Models import User, UserModel
from UserModel import UserModelCRUD
#from conftest import client  # Import your Pydantic schema
from sqlalchemy.ext.asyncio import AsyncSession

from conftest import TestSessionLocal

@pytest.mark.asyncio
async def test_create_user(async_session: AsyncSession):
    """Test user creation in the database."""

    user_crud = UserModelCRUD(session=async_session)
    # user_crud = UserModelCRUD(session=TestSessionLocal)
    
    # Create test user
    test_user = User(name="test_user_1", password="passw1", amount=0)
    new_user = await user_crud.create(data=test_user)

    assert new_user is not None
    assert new_user.user_name == "test_user_1"
    assert new_user.user_id > 0

    # Check if user exists in DB
    db_user = await async_session.get(UserModel, new_user.user_id)
    assert db_user is not None
    assert db_user.user_name == "test_user_1"

@pytest.mark.asyncio
async def test_get_user(async_session: AsyncSession):
    """Test retrieving a user from the database."""

    user_crud = UserModelCRUD(session=async_session)
    
#     # Retrieve user from DB
    retrieved_user = await user_crud.get_user(user_id=1)
    
    assert retrieved_user is not None
    assert retrieved_user.user_id > 0
