import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings
from app.db.base import Base

# Use the same database for simplicity in this environment, 
# or use a test database URL if available.
# Ideally: settings.DATABASE_URL + "_test"
TEST_DATABASE_URL = settings.DATABASE_URL

@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.asyncio
async def test_user_flow(client):
    # 1. Register User
    response = await client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "email": "flowtest@example.com",
            "password": "password123",
            "full_name": "Flow Test User"
        },
    )
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.json()
        assert data["email"] == "flowtest@example.com"
        assert "id" in data

    # 2. Login
    login_res = await client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={
            "username": "flowtest@example.com",
            "password": "password123"
        },
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Get Profile
    profile_res = await client.get(f"{settings.API_V1_STR}/auth/me", headers=headers)
    assert profile_res.status_code == 200
    profile_data = profile_res.json()
    assert profile_data["email"] == "flowtest@example.com"
    
    # 4. Update Profile
    update_data = {
        "age": 25,
        "gender": "female",
        "bio": "Flow test bio"
    }
    update_res = await client.put(f"{settings.API_V1_STR}/users/me", headers=headers, json=update_data)
    assert update_res.status_code == 200
    updated_data = update_res.json()
    assert updated_data["age"] == 25
    assert updated_data["bio"] == "Flow test bio"

