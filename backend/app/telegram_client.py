import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError, FloodWaitError, RPCError, PasswordHashInvalidError
from .config import settings
import redis.asyncio as redis

logger = logging.getLogger("telegram_auth")  # Use a clear logger name

class TelegramAuthClient:
    """
    Encapsulates Telegram authentication logic using Telethon.
    Session data is stored in Redis between steps.
    """

    def __init__(self):
        self.api_id = settings.TELEGRAM_API_ID
        self.api_hash = settings.TELEGRAM_API_HASH

    async def _create_client(self, session_str: str | None = None) -> TelegramClient:
        """Create and connect a TelegramClient using an existing session or a new one."""
        client = TelegramClient(
            StringSession(session_str) if session_str else StringSession(),
            self.api_id,
            self.api_hash
        )
        await client.connect()
        return client

    async def send_code(self, phone: str, redis_client: redis.Redis) -> str:
        """
        Send a verification code to the given phone number.
        Save the session string and phone_code_hash in Redis.
        """
        client = None
        try:
            client = await self._create_client()
            logger.info(f"Sending verification code to {phone}...")
            
            result = await client.send_code_request(phone)
            session_str = client.session.save()

            # Save session and phone_code_hash in Redis
            await redis_client.set(f"tg:session:{phone}", session_str)
            await redis_client.set(f"tg:hash:{phone}", result.phone_code_hash)

            logger.info(f"Code sent successfully to {phone}.")
            return result.phone_code_hash
        finally:
            if client:
                await client.disconnect()

    async def sign_in(self, phone: str, code: str, redis_client: redis.Redis) -> str:
        """
        Verify the code and sign in the user.
        Returns a new session string.
        """
        session_str = await redis_client.get(f"tg:session:{phone}")
        phone_code_hash_bytes = await redis_client.get(f"tg:hash:{phone}")

        if not session_str or not phone_code_hash_bytes:
            raise ValueError("Session or phone_code_hash not found. Please request a new code.")
        
        phone_code_hash = phone_code_hash_bytes  # Redis returns bytes

        client = None
        try:
            client = await self._create_client(session_str)
            logger.info(f"Attempting to sign in {phone} with verification code.")
            
            result = await client.sign_in(phone=phone, code=code, phone_code_hash=phone_code_hash)
            new_session_str = client.session.save()
            await redis_client.set(f"tg:session:{phone}", new_session_str)
            await redis_client.delete(f"tg:hash:{phone}")

            logger.info(f"Sign-in successful for {phone}.")
            return new_session_str
        finally:
            if client:
                await client.disconnect()

    async def check_2fa_password(self, phone: str, password: str, redis_client: redis.Redis) -> str:
        """
        Complete sign-in with a 2FA password using the same session.
        Returns a new session string.
        """
        session_str = await redis_client.get(f"tg:session:{phone}")
        if not session_str:
            raise ValueError("Session not found. Please request a new code.")

        client = None
        try:
            client = await self._create_client(session_str)
            
            # Telethon knows 2FA is required based on the session state
            await client.sign_in(password=password)
            
            new_session_str = client.session.save()
            await redis_client.set(f"tg:session:{phone}", new_session_str)

            logger.info(f"2FA sign-in successful for {phone}.")
            return new_session_str
        finally:
            if client:
                await client.disconnect()
