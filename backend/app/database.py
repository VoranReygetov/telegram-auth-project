from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings
from typing import AsyncGenerator

# Create async DB engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Show SQL queries in logs
)

# Create async session factory
async_session = async_sessionmaker(async_engine, expire_on_commit=False)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
async def get_db():
    async with async_session() as session:
        yield session
