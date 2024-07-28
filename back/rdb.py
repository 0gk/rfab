import redis.asyncio as redis
import config 

r = None

def rInit():
    return redis.Redis(
        host=config.REIDS_HOST,
        port=config.REIDS_PORT,
        db=0,
        decode_responses=True
    )

