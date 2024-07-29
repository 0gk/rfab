import asyncio
import sys

sys.path.append('/home/fab/rfab/back/')

import config 
from rdb import rInit


r = rInit()

sample = '''
hdd processed: 1234
     fan1 RPM: 1001
     fan2 RPM: 997
'''

max_jbod_idx = 5

async def statgen(plid):
    for jbod_idx in range(max_jbod_idx):
        await r.hset(f'{config.REDIS_JBOD_STAT_KEY_PREFIX:}:{plid}', f'{jbod_idx}', sample)

loop = asyncio.get_event_loop()
loop.run_until_complete(statgen(1))

