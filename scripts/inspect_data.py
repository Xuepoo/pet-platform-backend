import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.report import Report
from app.models.pet import Pet

async def inspect():
    async with SessionLocal() as db:
        print("--- Reports ---")
        result = await db.execute(select(Report))
        reports = result.scalars().all()
        for report in reports:
            print(f"ID: {report.id}, Pet: {report.pet_name}, Type: {report.report_type}, Status: {report.status}, Desc: {report.description}")
            
        print("\n--- Pets ---")
        result = await db.execute(select(Pet))
        pets = result.scalars().all()
        for pet in pets:
            print(f"ID: {pet.id}, Name: {pet.name}, Species: {pet.species}, Status: {pet.status}, Desc: {pet.description}")

if __name__ == "__main__":
    asyncio.run(inspect())