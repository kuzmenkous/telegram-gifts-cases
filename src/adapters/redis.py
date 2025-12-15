from redis.asyncio import Redis

from src.core.config import settings

redis = Redis(
    host="redis", password=settings.redis.password, decode_responses=True
)
