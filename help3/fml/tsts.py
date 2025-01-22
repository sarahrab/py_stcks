import pytest

from main import UserAccount, Role, login, User


@pytest.mark.asyncio
async def test_login():
    ua = UserAccount(name="ty", user_id=100, amount=2000, role_id=0, role=Role.ADMIN)
    res = await login(User(name="ty", password="hhh"))
    assert res.user_id == ua.user_id