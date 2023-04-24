from typing import Union, Dict, Any, Annotated
import asyncio
import json 

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from redis_om.model import NotFoundError

from rmodels import Plant, Jbod, Slot 
from rdb import r, rInit
from exceptions import RfabIncorrectDataFormat
import settings as s

app = FastAPI()

origins = [
       # 'http://fab.rlab.ru:9090/',
        '*',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def logErr(msg):
    print(f'ERROR: {msg}')
    await r.publish(s.REDIS_ERROR_CH_NAME, f'ERROR: {msg}')


async def log(msg):
    print(msg)
    await r.publish(s.REDIS_LOG_CH_NAME, f'{msg}')


# Async reader from redis channel
async def reader(chName: str):
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(chName,)
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                try:
                    yield json.loads(message['data'])
                except json.decoder.JSONDecodeError as em:
                    await logErr(em) # Bubbling an exception outside the loop will break it 


# Async reader from channels, matching the pattern
async def preader(chNamePattern: str):
    async with r.pubsub() as pubsub:
        await pubsub.psubscribe(chNamePattern,)
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                try:
                    yield message['channel'], json.loads(message['data'])
                except json.decoder.JSONDecodeError as em:
                    await logErr(em) # Bubbling an exception outside the loop will break it 


async def frontendUpdater(plid: str):
    counter = 0
    async for updateData in reader(f'{s.REDIS_PLANT_UPDATE_CH_PREFIX}:{plid}'):
        counter += 1
        yield {'event': 'message', 'data': json.dumps({'type': updateData['type'], 'data': updateData['data']}), 'id': counter}


# https://fastapi.tiangolo.com/tutorial/body-updates/#partial-updates-with-patch
# Pydantic model.copy(update=update_data) don't support nested models
def updateModel(model: Union[Plant, Jbod, Slot], newData: Dict[str, Any]):
    for key in newData:
        if isinstance(newData[key], dict):
            if isinstance(model, dict):
                updateModel(model[key], newData[key])
            else:
                updateModel(getattr(model, key), newData[key])
        else:
            if not hasattr(model, key):
                raise RfabIncorrectDataFormat(f'Attempting to set a value for a non-existent model attribute {key}')
            setattr(model, key, newData[key])


# Updates model based on redis channel updates
async def modelUpdater(chNamePattern: str):
    async for chName, newData in preader(chNamePattern):
        try:
            plid = chName.split(':')[-1]
            if newData['type'] == 'state':
                plant = Plant.parse_obj(newData['data'])
                plant.pk = plid
                plant.save()
            elif newData['type'] == 'update':
                try:
                    plant = Plant.get(plid)
                    updateModel(plant, newData['data'])
                    plant.save()
                except NotFoundError:
                    raise RfabIncorrectDataFormat(f'Appropriate plant for cannel {chName=} {plid=} not found in DB')
            elif newData['type'] == 'jbodstat':
                for jbod_idx in newData['data']:
                    jbodstat_str = json.dumps(newData['data'][jbod_idx])
                    await r.hset(f'{s.REDIS_JBOD_STAT_KEY_PREFIX}:{plid}', jbod_idx, jbodstat_str)
            elif newData['type'] == 'dutinfo':
                for jbod_idx in newData['data']:
                    for slot_idx in newData['data'][jbod_idx]:
                        dutinfo_str = json.dumps(newData['data'][jbod_idx][slot_idx])
                        await r.hset(f'{s.REDIS_DUT_INFO_KEY_PREFIX}:{plid}', f'{jbod_idx}:{slot_idx}', dutinfo_str)
            else:
                raise RfabIncorrectDataFormat('Incorrect data type')

        except RfabIncorrectDataFormat as em:
            await logErr(f'{em}')
        except KeyError as em:
            await logErr(f'No key {em} in message found')


# === STARTUP AND SHUTDOWN ============================================


@app.on_event('startup')
async def startup():
    global r
    r = await rInit() 

    # Run update state from channels
    asyncio.create_task(modelUpdater(s.REDIS_PLANT_UPDATE_CH_PREFIX + '*'))

    await log('STARTED')


@app.on_event('shutdown')
async def shutdown():
    await r.close()

    await log('STOPPED')


# === ROUTES =============================================


@app.get('/')
async def root():
    return {'message': 'What are you fumbling around here?'}


@app.get('/plant/{plid}', response_model = Plant, response_model_exclude={'pk'}) # Things like this: response_model_exclude={'pk': True, 'jbods': {'__all__': {'pk',}}} sutable only for nested sets, lists or tuples, not for tested dicts
async def getPlant(plid: str):
    try:
        plant = Plant.get(plid)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f'No plant {plid=} found')
    return plant


@app.get('/sse/{plid}')
async def sse(plid: str):
    return EventSourceResponse(frontendUpdater(plid))


@app.get('/jbodstat/{plid}/{jbod_idx}')
async def getJbodStat(plid: str, jbod_idx: str):
    try:
        stat_json = await r.hget(f'{s.REDIS_JBOD_STAT_KEY_PREFIX}:{plid}', jbod_idx)
    except NotFoundError:
        stat_json = f'So far there is no statistic for jbod {jbod_idx} at {plid}'
    return JSONResponse(content=stat_json)


@app.get('/dutinfo/{plid}/{jbod_idx}/{slot_idx}')
async def getDutInfo(plid: str, jbod_idx: str, slot_idx: str):
    try:
        info_json = await r.hget(f'{s.REDIS_DUT_INFO_KEY_PREFIX}:{plid}', f'{jbod_idx}:{slot_idx}')
    except NotFoundError:
        info_json = f'There is no additional information for the slot {plid}/{jbod_idx}/{slot_idx}'
    return JSONResponse(content=info_json)


@app.post('/action/{plid}')
async def publish(plid: str, request: Request):
    action = await request.body()
    await r.publish(f'{s.REDIS_ACTION_CH_PREFIX}:{plid}', action)
    return 'Action requested' 


# This model needed only for /docs, for create correct input form
class ModelUpdate(BaseModel):
    type: str
    data: Plant


@app.post('/publish')
async def publish(update: ModelUpdate, request: Request):
    update = await request.body()
    await r.publish(f'{s.REDIS_PLANT_UPDATE_CH_PREFIX}:1', update)
    return '-> published' 
