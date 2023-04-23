import asyncio

import settings as s

from rdb import rInit


r = rInit()


sample = '''
     I/F:  SATA 6G
     Mfg:  HGST 0x218
   Model:  WDC WD160EDFZ-11AFWA0
     S/N:  2CG7AG4R
      FW:  81.00A81
    INFO:  7200 RPM, TCG/FDE, SANITIZE
Capacity:  31251759104 sectors (16.00 TB / 14.55 TiB ), sector 512b / 4096b
Power-On:  20 hours
  Helium:  OK (100%)
   SMART:  34'C, 68 reallocations, 8 pendings
   Notes:  n/a
'''

max_jbod_idx = 5
max_slot_idx = 20

async def dutgen(plid):
    for jbod_idx in range(max_jbod_idx):
        for slot_idx in range(max_slot_idx):
            await r.hset(f'{s.REDIS_DUT_INFO_KEY_PREFIX}:{plid}', f'{jbod_idx}:{slot_idx}', sample)

loop = asyncio.get_event_loop()
loop.run_until_complete(dutgen(1))

