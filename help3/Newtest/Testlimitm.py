import pytest
from httpx import AsyncClient
from main import app  # Import your FastAPI app

@pytest.mark.asyncio
async def test_rate_limiter():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Make two successful requests
        response1 = await client.get("/limited")
        assert response1.status_code == 200

        response2 = await client.get("/limited")
        assert response2.status_code == 200

        # Third request should be rate-limited
        response3 = await client.get("/limited")
        assert response3.status_code == 429
        assert response3.json() == {"detail": "Rate limit exceeded"}
