"""Update report description to match image."""

import asyncio
from sqlalchemy import select, update
from app.db.session import SessionLocal
from app.models.report import Report


async def fix_report_description():
    """Fix the description of 小白 report to match the dog image."""
    async with SessionLocal() as session:
        # Update the report
        result = await session.execute(
            update(Report)
            .where(Report.pet_name == '小白')
            .values(description='我家的小白狗走丢了！它是一只白色的梗犬，大约2岁，脖子上戴着蓝色项圈。最后一次见到它是在公园附近。如果有人看到它，请联系我，非常感谢！')
        )
        await session.commit()
        print(f"✅ Updated {result.rowcount} report(s)")


if __name__ == "__main__":
    asyncio.run(fix_report_description())
