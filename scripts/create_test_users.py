import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

TEST_USERS = [
    {
        "email": "admin@example.com",
        "full_name": "Admin User",
        "password": "adminpassword",
        "is_superuser": True
    },
    {
        "email": "user1@example.com",
        "full_name": "Alice Smith",
        "password": "password123",
        "is_superuser": False
    },
    {
        "email": "user2@example.com",
        "full_name": "Bob Jones",
        "password": "password123",
        "is_superuser": False
    },
    {
        "email": "miko@example.com",
        "full_name": "Miko Test",
        "password": "TestPass123!",
        "is_superuser": False
    }
]

async def create_users():
    async with SessionLocal() as db:
        print("Creating test users...")
        for user_data in TEST_USERS:
            stmt = select(User).where(User.email == user_data["email"])
            result = await db.execute(stmt)
            existing_user = result.scalars().first()
            
            if not existing_user:
                print(f"Creating user: {user_data['email']}")
                user = User(
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    is_superuser=user_data["is_superuser"],
                    is_active=True
                )
                db.add(user)
            else:
                print(f"User already exists: {user_data['email']}")
        
        await db.commit()
        print("Users created.")

if __name__ == "__main__":
    asyncio.run(create_users())