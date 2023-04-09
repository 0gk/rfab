from typing import Union, Dict, Any, Annotated
import asyncio
import json 

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse

from redis_om.model import NotFoundError
import redis.asyncio as redis

from rmodels import Plant, Jbod, Slot
from rdb import r
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
    await r.publish(s.ERROR_CH_NAME, f'ERROR: {msg}')


async def log(msg):
    print(msg)
    await r.publish(s.LOG_CH_NAME, f'{msg}')


# Async reader from redis channel
async def reader(chName: str):
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(chName,)
        counter = 0
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                try:
                    yield json.loads(message['data'])
                except json.decoder.JSONDecodeError as em:
                    await logErr(em) # Bubbling an exception outside the loop will break it 


async def frontendUpdater(chName: str, plant_id: str):
    counter = 0
    async for updateData in reader(chName):
        try:
            if plant_id == updateData['id']:
                counter += 1
                yield {'event': 'message', 'data': json.dumps({'type': updateData['type'], 'data': updateData['data']}), 'id': counter}
        except KeyError as em:
            await logErr(f'No key {em} in message found')


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
async def modelUpdater(chName: str):
    async for newData in reader(chName):
        try:
            if newData['type'] == 'state':
                plant = Plant.parse_obj(newData['data'])
                plant.pk = newData['id'] 
                plant.save()
            elif newData['type'] == 'update':
                try:
                    plant = Plant.get(newData['id'])
                    updateModel(plant, newData['data'])
                    plant.save()
                except NotFoundError:
                    raise RfabIncorrectDataFormat(f'Plant {newData["id"]} not found in DB')
            else:
                raise RfabIncorrectDataFormat('Incorrect data type')
        except RfabIncorrectDataFormat as em:
            await logErr(f'{em}')
        except KeyError as em:
            await logErr(f'No key {em} in message found')


@app.on_event('startup')
async def startup():
    global r
    #r = redis.from_url(s.REDIS_URL)
    r = redis.Redis(
            host=s.REIDS_HOST,
            port=s.REIDS_PORT,
            db=0,
            decode_responses=True
    )

    # Run update state from channels
    asyncio.create_task(modelUpdater(s.PLANT_UPDATE_CH_NAME))

    await log('STARTED')


@app.on_event('shutdown')
async def shutdown():
    await r.close()

    await log('STOPPED')


@app.get('/')
async def root():
    return {'message': 'What are you fumbling around here?'}


@app.get('/plant/{id}', response_model = Plant, response_model_exclude={'pk'}) # Things like this: response_model_exclude={'pk': True, 'jbods': {'__all__': {'pk',}}} sutable only for nested sets, lists or tuples, not for tested dicts
async def getPlant(id: str):
    try:
        plant = Plant.get(id)
    except NotFoundError:
        raise HTTPException(status_code=404, detail=f'No plant {id=} found')
    return plant


@app.get('/sse/{id}')
async def sse(id: str):
    return EventSourceResponse(frontendUpdater(s.PLANT_UPDATE_CH_NAME, id))


# This model needed only for /docs create right form
class ModelUpdate(BaseModel):
    type: str
    id: str
    data: Dict[str, Plant]


@app.post('/publish')
async def publish(update: ModelUpdate, request: Request):
    update = await request.body()
    print(update)
    await r.publish(s.PLANT_UPDATE_CH_NAME, update)
    return '-> published' 


#@app.patch("/plant/update/{pk}")
#async def updatePlant(pk: str, newData: Dict[str, Any]):
#    plant = Plant.get(pk)
#    updateModel(plant, newData)
#    plant.save()
#    return plant

