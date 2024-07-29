from typing import Union, Dict, Any, Annotated
import asyncio
import json 

from pydantic import BaseModel, ValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from sse_starlette.sse import EventSourceResponse

from pymodels import Plant, Jbod, Slot 
from rdb import r, rInit
from exceptions import RfabIncorrectDataFormat
import config 

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
    await r.publish(config.REDIS_ERROR_CH_NAME, f'ERROR: {msg}')


async def log(msg):
    print(msg)
    await r.publish(config.REDIS_LOG_CH_NAME, f'{msg}')


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


async def frontendUpdater(plid: str, request: Request):
    counter = 0
    async for updateData in reader(f'{config.REDIS_PLANT_UPDATE_CH_PREFIX}:{plid}'):
        if await request.is_disconnected():
            break
        counter += 1
        yield {'event': 'message', 'data': json.dumps({'type': updateData['type'], 'data': updateData['data']}), 'id': counter}


# https://fastapi.tiangolo.com/tutorial/body-updates/#partial-updates-with-patch
# Pydantic model.copy(update=update_data) don't support nested models
def updateModel(model: Union[Plant, Jbod, Slot, Dict], newData: Dict[str, Any]):
    for key in newData:
        if isinstance(newData[key], dict):
            if isinstance(model, dict):
                if not key in model:
                    raise RfabIncorrectDataFormat(f'Attempting to set a value for a non-existent model attribute {key}')
                updateModel(model[key], newData[key])
            else:
                if not hasattr(model, key):
                    raise RfabIncorrectDataFormat(f'Attempting to set a value for a non-existent model attribute {key}')
                updateModel(getattr(model, key), newData[key])
        else:
            if isinstance(model, dict):
                if not key in model:
                    raise RfabIncorrectDataFormat(f'Attempting to set a value for a non-existent model attribute {key}')
                model[key] = newData[key]
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
                plant = Plant.model_validate(newData['data'])
                await r.set(f'{config.REDIS_PLANT_MODEL_KEY_PREFIX}:{plid}', plant.model_dump_json())
            elif newData['type'] == 'update':
                plant_json = await r.get(f'{config.REDIS_PLANT_MODEL_KEY_PREFIX}:{plid}')
                if not plant_json:
                    raise RfabIncorrectDataFormat(f'Appropriate plant for cannel {chName=} {plid=} not found in DB')
                plant = Plant.model_validate_json(plant_json)
                updateModel(plant, newData['data'])
                await r.set(f'{config.REDIS_PLANT_MODEL_KEY_PREFIX}:{plid}', plant.model_dump_json())
            elif newData['type'] == 'jbodstat':
                for jbod_idx in newData['data']:
                    jbodstat_str = json.dumps(newData['data'][jbod_idx])
                    await r.hset(f'{config.REDIS_JBOD_STAT_KEY_PREFIX}:{plid}', jbod_idx, jbodstat_str)
            elif newData['type'] == 'dutinfo':
                for jbod_idx in newData['data']:
                    for slot_idx in newData['data'][jbod_idx]:
                        dutinfo_str = json.dumps(newData['data'][jbod_idx][slot_idx])
                        await r.hset(f'{config.REDIS_DUT_INFO_KEY_PREFIX}:{plid}', f'{jbod_idx}:{slot_idx}', dutinfo_str)
            else:
                raise RfabIncorrectDataFormat('Incorrect data type')

        except RfabIncorrectDataFormat as em:
            await logErr(f'modelUpdater: {em}')
        except KeyError as em:
            await logErr(f'modelUpdater: No key {em} in message found')
        except ValidationError as em:
            await logErr(f'modelUpdater: {em}')


# === STARTUP AND SHUTDOWN ============================================


@app.on_event('startup')
async def startup():
    global r
    r = await rInit() 

    # Run update state from channels
    asyncio.create_task(modelUpdater(config.REDIS_PLANT_UPDATE_CH_PREFIX + '*'))

    await log('STARTED')


@app.on_event('shutdown')
async def shutdown():
    await r.close()

    await log('STOPPED')


# === ROUTES =============================================


@app.get('/')
async def root():
    return {'message': 'What are you fumbling around here?'}


@app.get('/plant/{plid}') 
async def getPlant(plid: str):
    plant_json = await r.get(f'{config.REDIS_PLANT_MODEL_KEY_PREFIX}:{plid}')
    if not plant_json:
        raise HTTPException(status_code=404, detail=f'No plant {plid=} found')
    return Response(content=plant_json, media_type="application/json")


@app.get('/sse/{plid}')
async def sse(plid: str, request: Request):
    return EventSourceResponse(frontendUpdater(plid, request))


@app.get('/jbodstat/{plid}/{jbod_idx}')
async def getJbodStat(plid: str, jbod_idx: str):
    stat_json = await r.hget(f'{config.REDIS_JBOD_STAT_KEY_PREFIX}:{plid}', jbod_idx)
    if not stat_json:
        stat_json = f'So far there is no statistic for jbod {jbod_idx} at {plid}'
    return JSONResponse(content=stat_json)


@app.get('/dutinfo/{plid}/{jbod_idx}/{slot_idx}')
async def getDutInfo(plid: str, jbod_idx: str, slot_idx: str):
    info_json = await r.hget(f'{config.REDIS_DUT_INFO_KEY_PREFIX}:{plid}', f'{jbod_idx}:{slot_idx}')
    if not info_json:
        info_json = f'There is no additional information for the slot {plid}/{jbod_idx}/{slot_idx}'
    return JSONResponse(content=info_json)


@app.post('/action/{plid}')
async def publish(plid: str, request: Request):
    action = await request.body()
    await r.publish(f'{config.REDIS_ACTION_CH_PREFIX}:{plid}', action)
    return 'Action requested' 


# This model needed only for /docs, for create correct input form
class ModelUpdate(BaseModel):
    type: str
    data: Plant


@app.post('/publish')
async def publish(update: ModelUpdate, request: Request):
    update = await request.body()
    await r.publish(f'{config.REDIS_PLANT_UPDATE_CH_PREFIX}:1', update)
    return '-> published' 
