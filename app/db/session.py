"""Database session configuration.

This module sets up the async SQLAlchemy engine and session factory
for database operations.
"""

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
print(f"Connecting to database: {settings.DATABASE_URL}")
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
