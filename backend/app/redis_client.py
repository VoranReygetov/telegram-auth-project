import redis.asyncio as redis
from .config import settings

# Create a Redis connection pool (to avoid creating new connection on every request)
redis_pool = redis.ConnectionPool.from_url(settings.REDIS_URL, decode_responses=True)

async def get_redis():
    """Dependency to get a Redis connection."""
    r = redis.Redis(connection_pool=redis_pool)
    try:
        yield r
    finally:
        await r.close()
