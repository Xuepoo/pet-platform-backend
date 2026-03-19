import asyncio
import sys
import os

# Add the parent directory to sys.path so we can import 'app'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select, delete
from app.db.session import SessionLocal
from app.models.user import User
from app.models.pet import Pet
from app.models.post import Post, Comment, PostMedia, PostLike, CommentLike
from app.models.report import Report
from app.models.application import Application
from app.models.favorite import PetFavorite
from app.core.security import get_password_hash
from datetime import datetime, timedelta

async def reseed_data():
    async with SessionLocal() as db:
        print("Cleaning up old data...")
        await db.execute(delete(PostMedia))
        await db.execute(delete(CommentLike))
        await db.execute(delete(Comment))
        await db.execute(delete(PostLike))
        await db.execute(delete(Post))
        await db.execute(delete(Application))
        await db.execute(delete(Report))
        await db.execute(delete(PetFavorite))
        await db.execute(delete(Pet))
        await db.commit()

        print("Ensuring users exist...")
        # Check miko
        result = await db.execute(select(User).where(User.email == "miko@example.com"))
        miko = result.scalars().first()
        if not miko:
            miko = User(
                email="miko@example.com",
                full_name="Miko Test",
                hashed_password=get_password_hash("TestPass123!"),
                is_active=True
            )
            db.add(miko)
        
        # Check admin
        result = await db.execute(select(User).where(User.email == "admin@example.com"))
        admin = result.scalars().first()
        if not admin:
            admin = User(
                email="admin@example.com",
                full_name="Admin User",
                hashed_password=get_password_hash("adminpassword"),
                is_superuser=True,
                is_active=True
            )
            db.add(admin)
        
        await db.commit()
        await db.refresh(miko)
        await db.refresh(admin)
        
        miko_id = miko.id
        admin_id = admin.id

        print("Creating Pets with IMAGES...")
        pets_to_create = [
            Pet(
                name="Buddy",
                species="Dog",
                breed="Golden Retriever",
                age=3,
                description="Friendly and energetic Golden Retriever looking for a loving family! Loves fetch and swimming.",
                status="available",
                gender="male",
                size="large",
                image_url="/images/pets/buddy.jpg",
                owner_id=admin_id
            ),
            Pet(
                name="Luna",
                species="Cat",
                breed="Persian",
                age=2,
                description="Beautiful white Persian cat, very calm and affectionate. Requires daily grooming.",
                status="available",
                gender="female",
                size="medium",
                image_url="/images/pets/luna.jpg",
                owner_id=admin_id
            ),
            Pet(
                name="Charlie",
                species="Bird",
                breed="Parrot",
                age=5,
                description="Talkative and colorful parrot. Knows how to say 'Hello' and mimic sounds.",
                status="available",
                gender="male",
                size="small",
                image_url="/images/pets/charlie.jpg",
                owner_id=admin_id
            ),
            Pet(
                name="Rocky",
                species="Dog",
                breed="Bulldog",
                age=4,
                description="Calm and friendly Bulldog. Loves naps and short walks.",
                status="available",
                gender="male",
                size="medium",
                image_url="/images/pets/rocky.jpg",
                owner_id=admin_id
            ),
            Pet(
                name="Bella",
                species="Dog",
                breed="Labrador",
                age=1,
                description="Playful puppy full of energy. Needs training but very smart.",
                status="adopted",
                gender="female",
                size="large",
                image_url="/images/pets/bella.jpg",
                owner_id=admin_id
            )
        ]
        
        for p in pets_to_create:
            db.add(p)
        await db.commit()
        
        # Refresh to get IDs
        pets = {}
        for p in pets_to_create:
            await db.refresh(p)
            pets[p.name] = p.id # Store ID only

        print("Creating Reports (Lost & Found) in Chinese...")
        # Note: image_url needs to point to existing images
        reports_to_create = [
            Report(
                report_type="lost",
                pet_name="小白 (Xiao Bai) - Samoyed",
                location="朝阳公园 (Chaoyang Park)",
                description="我的萨摩耶小白昨天在朝阳公园附近走丢了。它很友善，脖子上有一个红色的项圈。如果看到请联系我！",
                contact_info="13800138000",
                status="open",
                image_url="/images/reports/found_dog.jpg", # Using existing
                user_id=miko_id
            ),
            Report(
                report_type="found",
                pet_name="橘猫 (Orange Cat)",
                location="上海图书馆 (Shanghai Library)",
                description="在上海图书馆附近发现一只橘猫，看起来很饿。没有项圈。",
                contact_info="WeChat: catfinder",
                status="open",
                image_url="/images/reports/lost_bird.jpg", # Using existing
                user_id=admin_id
            )
        ]
        for r in reports_to_create:
            db.add(r)
        
        print("Creating Feed Posts in Chinese...")
        posts_to_create = [
            Post(
                title="今天带狗狗去公园玩了",
                content="天气真好，Buddy 玩得很开心！\n\n![Buddy](/images/pets/buddy.jpg)\n\n大家周末都带宠物去哪里玩呢？",
                author_id=miko_id,
                created_at=datetime.utcnow() - timedelta(hours=2)
            ),
            Post(
                title="关于猫咪护理的小知识",
                content="这里有一些关于给波斯猫梳毛的建议...\n\n1. 每天梳理\n2. 使用针梳\n3. 注意眼睛周围的清洁",
                author_id=admin_id,
                created_at=datetime.utcnow() - timedelta(days=1)
            )
        ]
        for post in posts_to_create:
            db.add(post)
        
        await db.commit()

        print("Creating Applications for Miko...")
        apps_to_create = [
            Application(
                pet_id=pets["Luna"],
                user_id=miko_id,
                message="I would love to adopt Luna! She matches my lifestyle perfectly.",
                status="pending",
                created_at=datetime.utcnow()
            ),
            Application(
                pet_id=pets["Bella"],
                user_id=miko_id,
                message="Is Bella still available? She is so cute!",
                status="rejected", # Because she's adopted
                created_at=datetime.utcnow() - timedelta(days=2)
            )
        ]
        for app in apps_to_create:
            db.add(app)
        
        await db.commit()
        print("Data reseeded successfully!")

if __name__ == "__main__":
    asyncio.run(reseed_data())
