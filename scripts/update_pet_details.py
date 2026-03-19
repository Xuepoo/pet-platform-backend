import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.pet import Pet

async def update_pet_data():
    async with SessionLocal() as session:
        # Define updates
        updates = {
            1: {"gender": "male", "size": "large", "image_url": "https://images.unsplash.com/photo-1552053831-71594a27632d?w=800"}, # Buddy
            2: {"gender": "female", "size": "medium", "image_url": "https://images.unsplash.com/photo-1513245543132-31f507417b26?w=800"}, # Luna
            3: {"gender": "male", "size": "small", "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=800"}, # Mochi
            4: {"gender": "male", "size": "medium", "image_url": "https://images.unsplash.com/photo-1573865526739-10659fec78a5?w=800"}, # Oliver
            5: {"gender": "male", "size": "large", "image_url": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?w=800"}, # Max
        }

        for pet_id, data in updates.items():
            result = await session.execute(select(Pet).where(Pet.id == pet_id))
            pet = result.scalars().first()
            if pet:
                pet.gender = data["gender"]
                pet.size = data["size"]
                pet.image_url = data["image_url"]
                session.add(pet)
                print(f"Updated {pet.name}")
        
        await session.commit()

if __name__ == "__main__":
    asyncio.run(update_pet_data())