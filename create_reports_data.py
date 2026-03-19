"""Create sample lost/found pet reports with Chinese content."""

import asyncio
from sqlalchemy import select
from app.db.session import SessionLocal
from app.models.user import User
from app.models.report import Report


async def create_sample_reports():
    """Create sample lost/found pet reports."""
    async with SessionLocal() as session:
        # Get test users
        result = await session.execute(
            select(User).where(User.email.in_(['miko@example.com', 'sarah@example.com', 'alex@example.com']))
        )
        users = result.scalars().all()
        
        if not users:
            print("No test users found. Please run initial_data.py first.")
            return
        
        user_dict = {user.email: user for user in users}
        
        # Sample reports with Chinese content and pet images
        reports_data = [
            {
                "pet_name": "小白",
                "report_type": "lost",
                "description": "我家的小白狗走丢了！它是一只白色的梗犬，大约2岁，脖子上戴着蓝色项圈。最后一次见到它是在公园附近。如果有人看到它，请联系我，非常感谢！",
                "location": "北京市朝阳区望京公园",
                "contact_info": "13800138001",
                "image_url": "https://images.dog.ceo/breeds/terrier-kerryblue/n02093859_2225.jpg",
                "status": "open",
                "user": user_dict['miko@example.com']
            },
            {
                "pet_name": "巧克力",
                "report_type": "found",
                "description": "在小区门口发现一只棕色的拉布拉多犬，看起来很友好，没有项圈。它可能走失了，现在暂时在我家，希望主人看到后尽快联系我。",
                "location": "上海市浦东新区世纪公园",
                "contact_info": "13900139002",
                "image_url": "https://images.dog.ceo/breeds/basenji/n02110806_3903.jpg",
                "status": "open",
                "user": user_dict['sarah@example.com']
            },
            {
                "pet_name": "球球",
                "report_type": "lost",
                "description": "我的金毛球球不见了！它3岁了，非常温顺，最后在小区附近的超市门口见到。它脖子上有红色项圈，背上有个黑色斑点。如果您看到它，请一定联系我！",
                "location": "广州市天河区体育中心",
                "contact_info": "13700137003",
                "image_url": "https://images.dog.ceo/breeds/stbernard/n02109525_10908.jpg",
                "status": "open",
                "user": user_dict['alex@example.com']
            },
            {
                "pet_name": "小黑",
                "report_type": "found",
                "description": "捡到一只黑色的小狗，看起来像是柯基和腊肠犬的混血，非常可爱。在地铁站附近发现的，希望主人快点来认领。",
                "location": "深圳市南山区科技园",
                "contact_info": "13600136004",
                "image_url": "https://images.dog.ceo/breeds/waterdog-spanish/20180706_194432.jpg",
                "status": "open",
                "user": user_dict['miko@example.com']
            },
            {
                "pet_name": "多多",
                "report_type": "lost",
                "description": "寻找我的爱犬多多！它是一只灰色的雪纳瑞，5岁，耳朵做了断尾。昨天晚上在小区散步时走丢了。它很胆小，请不要吓到它。",
                "location": "杭州市西湖区文三路",
                "contact_info": "13500135005",
                "image_url": "https://images.dog.ceo/breeds/dingo/n02115641_4601.jpg",
                "status": "open",
                "user": user_dict['sarah@example.com']
            },
            {
                "pet_name": "旺财",
                "report_type": "found",
                "description": "在公园里发现一只中型犬，看起来像哈士奇混血，蓝色眼睛，非常漂亮。它很亲人，现在在我家暂住。主人看到请联系我。",
                "location": "成都市武侯区人民公园",
                "contact_info": "13400134006",
                "image_url": "https://images.dog.ceo/breeds/whippet/n02091134_12341.jpg",
                "status": "resolved",
                "user": user_dict['alex@example.com']
            }
        ]
        
        # Create reports
        for report_data in reports_data:
            user = report_data.pop('user')
            report = Report(**report_data, user_id=user.id)
            session.add(report)
        
        await session.commit()
        print(f"✅ Created {len(reports_data)} sample reports")


if __name__ == "__main__":
    asyncio.run(create_sample_reports())
