import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User
from app.models.pet import Pet
from app.models.report import Report

PETS_DATA = [
    {
        "name": "Buddy",
        "species": "Dog",
        "breed": "Golden Retriever",
        "age": 3,
        "description": "Friendly and energetic Golden Retriever looking for a loving family! Loves fetch and swimming.",
        "status": "available",
        "gender": "male",
        "size": "large",
        "image_url": "/images/pets/buddy.jpg"
    },
    {
        "name": "Luna",
        "species": "Cat",
        "breed": "Persian",
        "age": 2,
        "description": "Beautiful white Persian cat, very calm and affectionate. Requires daily grooming.",
        "status": "available",
        "gender": "female",
        "size": "medium",
        "image_url": "/images/pets/luna.jpg"
    },
    {
        "name": "Charlie",
        "species": "Bird",
        "breed": "Parrot",
        "age": 5,
        "description": "Talkative and colorful parrot. Knows how to say 'Hello' and mimic sounds.",
        "status": "available",
        "gender": "male",
        "size": "small",
        "image_url": "/images/pets/charlie.jpg"
    },
    {
        "name": "Rocky",
        "species": "Dog",
        "breed": "Bulldog",
        "age": 4,
        "description": "Calm and friendly Bulldog. Loves naps and short walks.",
        "status": "available",
        "gender": "male",
        "size": "medium",
        "image_url": "/images/pets/rocky.jpg"
    },
    {
        "name": "Bella",
        "species": "Dog",
        "breed": "Mixed",
        "age": 1,
        "description": "Playful puppy looking for a forever home. High energy and loves other dogs.",
        "status": "adopted",
        "gender": "female",
        "size": "small",
        "image_url": "/images/pets/bella.jpg"
    },
    {
        "name": "Max",
        "species": "Dog",
        "breed": "Labrador Retriever",
        "age": 2,
        "description": "Loyal black Lab who loves swimming and hiking.",
        "status": "pending",
        "gender": "male",
        "size": "large",
        "image_url": "/images/pets/max.jpg"
    }
]

REPORTS_DATA = [
    {
        "pet_name": "Tweety",
        "description": "My parrot flew away yesterday near Central Park. He is green with a red beak.",
        "location": "Central Park, NY",
        "report_type": "lost",
        "status": "open",
        "image_url": "/images/reports/lost_bird.jpg",
        "contact_info": "555-0101"
    },
    {
        "pet_name": "Found Dog",
        "description": "Found a bulldog wandering near Main St. No collar. Very friendly.",
        "location": "Main St, Springfield",
        "report_type": "found",
        "status": "open",
        "image_url": "/images/reports/found_dog.jpg",
        "contact_info": "555-0102"
    }
]

async def create_posts():
    async with SessionLocal() as db:
        print("Fetching users...")
        # Get users
        stmt = select(User).where(User.email.in_(['miko@example.com', 'user1@example.com', 'user2@example.com']))
        result = await db.execute(stmt)
        users = {u.email: u for u in result.scalars().all()}
        
        if not users:
            print("No users found! Please run create_test_users.py first.")
            return

        miko = users.get('miko@example.com')
        user1 = users.get('user1@example.com')
        user2 = users.get('user2@example.com')
        
        # Create Pets
        print("Creating pets...")
        for i, pet_data in enumerate(PETS_DATA):
            # Distribute ownership
            owner = miko if i % 2 == 0 else user1
            if not owner: owner = list(users.values())[0]
            
            pet = Pet(**pet_data, owner_id=owner.id)
            db.add(pet)
            
        # Create Reports
        print("Creating reports...")
        if miko:
            report1 = Report(**REPORTS_DATA[0], user_id=miko.id)
            db.add(report1)
        
        if user1:
            report2 = Report(**REPORTS_DATA[1], user_id=user1.id)
            db.add(report2)
            
        await db.commit()
        print("Sample posts created.")

if __name__ == "__main__":
    asyncio.run(create_posts())