import logging
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, FloodWaitError, PasswordHashInvalidError
from schemas.requests import PhoneRequest, CodeVerifyRequest, TwoFAVerifyRequest
from app.telegram_client import TelegramAuthClient
from app.database import get_db
from app.redis_client import get_redis
from app.crud import get_or_create_user
from utils import security
from utils.limiter import limiter

logger = logging.getLogger("uvicorn")
router = APIRouter()
CODE_HASH_TTL_SECONDS = 300

@router.post("/send-code")
@limiter.limit("5/minute")
async def send_code(request: Request, data: PhoneRequest, redis_client: redis.Redis = Depends(get_redis)):
    """
    Send a verification code to the given phone number and store phone_code_hash in Redis.
    """
    client = TelegramAuthClient()
    try:
        phone_code_hash = await client.send_code(data.phone, redis_client)
        await redis_client.set(f"phone_code_hash:{data.phone}", phone_code_hash, ex=CODE_HASH_TTL_SECONDS)
        logger.info(f"Code sent to {data.phone}")
        return {"message": "Verification code sent successfully."}
    except FloodWaitError as e:
        logger.warning(f"FloodWaitError for {data.phone}: wait {e.seconds}s")
        raise HTTPException(status_code=429, detail=f"Too many requests. Please try again in {e.seconds} seconds.")
    except Exception as e:
        logger.error(f"Failed to send code to {data.phone}: {e}")
        raise HTTPException(status_code=400, detail="Failed to send verification code.")

@router.post("/verify-code")
@limiter.limit("10/minute")
async def verify_code(
    request: Request,
    data: CodeVerifyRequest,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    """
    Verify code, sign in user, return JWT token.
    If 2FA is required, returns a message to request 2FA password.
    """
    phone_code_hash = await redis_client.get(f"phone_code_hash:{data.phone}")
    if not phone_code_hash:
        raise HTTPException(status_code=400, detail="Verification code expired. Request a new one.")
    
    client = TelegramAuthClient()
    try:
        session_string = await client.sign_in(data.phone, data.code, redis_client)
        session_string_encrypted = security.encrypt_data(session_string)
        user = await get_or_create_user(db, data.phone, session_string_encrypted)
        await db.commit()

        await redis_client.delete(f"phone_code_hash:{data.phone}")
        access_token = security.create_access_token(data={"sub": user.phone})
        logger.info(f"User {data.phone} signed in successfully")
        return {"access_token": access_token, "token_type": "bearer"}

    except SessionPasswordNeededError:
        logger.info(f"2FA required for {data.phone}")
        return {"message": "2FA password required"}
    except PhoneCodeInvalidError:
        logger.warning(f"Invalid verification code for {data.phone}")
        raise HTTPException(status_code=400, detail="Invalid verification code.")
    except Exception as e:
        logger.error(f"Unexpected error during verify-code for {data.phone}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

@router.post("/verify-2fa")
@limiter.limit("5/minute")
async def verify_2fa(
    request: Request,
    data: TwoFAVerifyRequest,
    db: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis)
):
    """
    Verify 2FA password and complete sign-in, returning JWT token.
    """
    client = TelegramAuthClient()
    try:
        session_string = await client.check_2fa_password(data.phone, data.password, redis_client)
        session_string_encrypted = security.encrypt_data(session_string)
        user = await get_or_create_user(db, data.phone, session_string_encrypted)
        await db.commit()

        access_token = security.create_access_token(data={"sub": user.phone})
        logger.info(f"User {data.phone} signed in successfully with 2FA")
        return {"access_token": access_token, "token_type": "bearer"}

    except PasswordHashInvalidError:
        logger.warning(f"Invalid 2FA password for {data.phone}")
        raise HTTPException(status_code=400, detail="Incorrect 2FA password.")
    except Exception as e:
        logger.error(f"Unexpected error during verify-2fa for {data.phone}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error.")

