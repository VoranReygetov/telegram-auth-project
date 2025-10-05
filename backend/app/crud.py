from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from sqlalchemy import select


async def get_or_create_user(db: AsyncSession, phone: str, session_string_encrypted: bytes) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.phone == phone))
    user = result.scalars().first()
    if not user:
        user = models.User(phone=phone, session_string_encrypted=session_string_encrypted)
        db.add(user)
        await db.flush()
    return user
