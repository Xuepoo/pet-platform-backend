import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.pet import Pet

async def check_pets():
    async with SessionLocal() as session:
        result = await session.execute(select(Pet))
        pets = result.scalars().all()
        for pet in pets:
            print(f"ID: {pet.id}, Name: {pet.name}, Species: {pet.species}, Breed: {pet.breed}, Gender: {pet.gender}, Size: {pet.size}, Image: {pet.image_url}, Description: {pet.description}")

if __name__ == "__main__":
    asyncio.run(check_pets())