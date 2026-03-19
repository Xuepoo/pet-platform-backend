import asyncio
from sqlalchemy import delete
from app.db.session import SessionLocal
from app.models.report import Report
from app.models.pet import Pet
from app.models.application import Application
from app.models.favorite import PetFavorite

async def clean_data():
    async with SessionLocal() as db:
        print("Cleaning up database...")
        
        # Delete dependent tables first
        print("Deleting applications...")
        await db.execute(delete(Application))
        
        print("Deleting favorites...")
        await db.execute(delete(PetFavorite))
        
        print("Deleting reports...")
        await db.execute(delete(Report))
        
        print("Deleting pets...")
        await db.execute(delete(Pet))
        
        await db.commit()
        print("Database cleaned.")

if __name__ == "__main__":
    asyncio.run(clean_data())