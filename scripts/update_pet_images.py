import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.pet import Pet

async def update_pet_images():
    async with SessionLocal() as session:
        # 1. Update existing
        result = await session.execute(select(Pet))
        existing_pets = result.scalars().all()
        existing_names = {p.name for p in existing_pets}
        
        updates = {
            "Buddy": "/images/pets/buddy.jpg",
            "Luna": "/images/pets/luna.jpg",
            "Max": "/images/pets/max.jpg",
            "Bella": "/images/pets/bella.jpg",
            "Charlie": "/images/pets/charlie.jpg", 
            "Lucy": "/images/pets/lucy.jpg",
            "Rocky": "/images/pets/rocky.jpg",
        }
        
        for pet in existing_pets:
            if pet.name in updates:
                pet.image_url = updates[pet.name]
                print(f"Updating {pet.name}")
        
        # 2. Add missing
        missing_pets = [
            Pet(
                name="Bella",
                species="dog",
                breed="Beagle",
                age=1,
                description="Playful puppy looking for a forever home.",
                status="adopted",
                gender="female",
                size="medium",
                image_url="/images/pets/bella.jpg"
            ),
            Pet(
                name="Charlie",
                species="bird",
                breed="Parrot",
                age=5,
                description="Talkative and colorful parrot.",
                status="available",
                gender="male",
                size="small",
                image_url="/images/pets/charlie.jpg"
            ),
            Pet(
                name="Lucy",
                species="cat",
                breed="Maine Coon",
                age=3,
                description="Gentle giant. Very fluffy.",
                status="pending",
                gender="female",
                size="large",
                image_url="/images/pets/lucy.jpg"
            ),
            Pet(
                name="Rocky",
                species="dog",
                breed="Bulldog",
                age=2,
                description="Calm and friendly. Loves naps.",
                status="available",
                gender="male",
                size="medium",
                image_url="/images/pets/rocky.jpg"
            ),
        ]
        
        for new_pet in missing_pets:
            if new_pet.name not in existing_names:
                print(f"Adding new pet: {new_pet.name}")
                session.add(new_pet)
        
        await session.commit()
        print("Done updating/adding pets")

if __name__ == "__main__":
    asyncio.run(update_pet_images())