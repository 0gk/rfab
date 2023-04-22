import redis.asyncio as redis
import settings as s

r = None

def rInit():
    return redis.Redis(
        host=s.REIDS_HOST,
        port=s.REIDS_PORT,
        db=0,
        decode_responses=True
    )

