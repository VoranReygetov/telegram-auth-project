from pydantic_settings import BaseSettings
from typing import List
import json

class Settings(BaseSettings):
    TELEGRAM_API_ID: int
    TELEGRAM_API_HASH: str
    DATABASE_URL: str
    REDIS_URL: str
    
    SECRET_KEY: str
    ENCRYPTION_KEY: str
    
    CORS_ORIGINS_STR: str
    
    @property
    def CORS_ORIGINS(self) -> List[str]:
        return json.loads(self.CORS_ORIGINS_STR)

    class Config:
        env_file = ".env"

settings = Settings()

