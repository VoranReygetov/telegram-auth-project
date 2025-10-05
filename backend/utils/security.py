from cryptography.fernet import Fernet
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

# Encryption setup
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def encrypt_data(data: str) -> bytes:
    """Encrypt string data using Fernet."""
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data: bytes) -> str:
    """Decrypt Fernet encrypted bytes back to string."""
    return fernet.decrypt(encrypted_data).decode()

# JWT setup
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    """Create JWT access token with expiration."""
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
