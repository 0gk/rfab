import json 
import time

#import redis
import redis.asyncio as redis

r = redis.Redis()

max_slot_idx = 15
max_jbod_idx = 5

p = 0
while True:
    for jbod_idx in range(max_jbod_idx):
        for slot_idx in range(max_slot_idx):
            update = {"type": "update", "data": { "jbods": { jbod_idx: {"slots": { slot_idx: {"progress": p} }}}}}
            update_json = json.dumps(update)
            print(update)
            r.publish('rfab:update:1', update_json)
            time.sleep(1/300)
            p += 1
