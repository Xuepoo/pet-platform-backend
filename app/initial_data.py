import asyncio
import logging

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User
from app.models.pet import Pet
from app.core.security import get_password_hash
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def init_db() -> None:
    async with SessionLocal() as session:
        # Check if users exist
        result = await session.execute(select(User).limit(1))
        user = result.scalars().first()
        
        if not user:
            logger.info("Creating initial users")
            
            # Create superuser
            superuser = User(
                email="admin@example.com",
                full_name="Admin User",
                hashed_password=get_password_hash("admin123"),
                is_active=True,
                is_superuser=True,
            )
            session.add(superuser)
            
            # Create regular users
            user1 = User(
                email="user@example.com",
                full_name="Regular User",
                hashed_password=get_password_hash("user123"),
                is_active=True,
                is_superuser=False,
            )
            session.add(user1)
            await session.commit()
        else:
            logger.info("Users already exist")

        # Check if pets exist
        result = await session.execute(select(Pet).limit(1))
        pet = result.scalars().first()

        if not pet:
            logger.info("Creating initial pets")
            # Create pets
            pets = [
                Pet(
                    name="Buddy",
                    species="dog",
                    breed="Golden Retriever",
                    age=3,
                    description="Friendly and energetic Golden Retriever. Loves fetch!",
                    status="available",
                    gender="male",
                    size="large",
                    image_url="https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=500&q=60"
                ),
                Pet(
                    name="Luna",
                    species="cat",
                    breed="Siamese",
                    age=2,
                    description="Quiet and affectionate Siamese cat. Loves sunny spots.",
                    status="available",
                    gender="female",
                    size="small",
                    image_url="https://images.unsplash.com/photo-1513245543132-31f507417b26?auto=format&fit=crop&w=500&q=60"
                ),
                Pet(
                    name="Max",
                    species="dog",
                    breed="German Shepherd",
                    age=4,
                    description="Loyal and protective. Needs a large yard.",
                    status="available",
                    gender="male",
                    size="large",
                    image_url="https://images.unsplash.com/photo-1589941013453-ec89f33b5e95?auto=format&fit=crop&w=500&q=60"
                ),
                Pet(
                    name="Bella",
                    species="dog",
                    breed="Beagle",
                    age=1,
                    description="Playful puppy looking for a forever home.",
                    status="adopted",
                    gender="female",
                    size="medium",
                    image_url="https://images.unsplash.com/photo-1537151608828-ea2b11777ee8?auto=format&fit=crop&w=500&q=60"
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
                    image_url="https://images.unsplash.com/photo-1552728089-57bdde30ebd1?auto=format&fit=crop&w=500&q=60"
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
                    image_url="https://images.unsplash.com/photo-1533738363-b7f9aef128ce?auto=format&fit=crop&w=500&q=60"
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
                    image_url="https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=500&q=60"
                ),
            ]
            
            for pet in pets:
                session.add(pet)
                
            await session.commit()
            logger.info("Initial pets created")
        else:
            logger.info("Pets already exist")

if __name__ == "__main__":
    asyncio.run(init_db())
