import redis.asyncio as redis
from config import settings 

r = None

def rInit():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        decode_responses=True
    )

