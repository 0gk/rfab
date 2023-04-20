from typing import Optional, Dict 
from enum import Enum
from abc import ABC

from redis_om import get_redis_connection, EmbeddedJsonModel, JsonModel, Field, Migrator

import settings as s

redis = get_redis_connection(
    host = s.REIDS_HOST,
    port = s.REIDS_PORT,
    #password='lksjdflkmsaclkasuoirwjaoifdewu798432u09ei3domsadr8=====>jflsamfoiweuyrosiajowau82098570',
    #decode_responses=True,
)

class BaseJsonModel(JsonModel, ABC):
    class Meta:
        global_key_prefix = s.REDIS_OM_GLOBAL_KEY_PREFIX
        database = redis

    # Cant hide pk from responce  through "class Config fields" because bug when get models from DB appiars - the key in the model received does not match the key in the database. Seems just new key generated each time. 


class BaseEmbeddedJsonModel(EmbeddedJsonModel, ABC):
    class Config:
        fields = {'pk': {'exclude': True},}


class Slot(BaseEmbeddedJsonModel):

    class State(Enum):
        NA = 0
        EMPTY = 1
        DISABLED = 2
        ACTIVE = 3
        INACTIVE = 4

    class Statuscode(Enum):
        NA = 0
        OK = 1
        ERR = 2

    class Interface(Enum):
        NA = 0
        SAS = 1
        SATA = 2
        NVME = 3

    class Grade(Enum):
        NA = 0
        HIGH = 1
        MEDIUM = 2
        LOW = 3

    idx: int #2-значный номер слота
    state: State
    status: str #свободная строка с некой инфой о состоянии
    scode: Statuscode
    progress: int #0 - не применимо, либо 100 - 10000 = 0.01 - 100.00%
    mdl: str
    sn: str
    itf: Interface 
    link: str #скорость интерфейсного линка
    grade: Grade 


class Jbod(BaseEmbeddedJsonModel):

    class State(Enum):
        NA = 0
        ONLINE = 1
        OFFLINE = 2

    idx: int
    wwn0: str #16 ASCII HEX
    wwn1: str #(16 ASCII HE)
    sasaddr: str #(16 ASCII HEX
    mdl: str #ASCII строка
    sn: str #ASCII строка
    fw: str #ASCII строка
    state: State 
    descr: str #(ASCII строка разумно-неопределённой длины)
    slots: Optional[Dict[str, Slot]]

    @property
    def wwn():
        return f'{self.wwn0}:{self.wwn1}'


class Plant(BaseJsonModel):
    owner: Optional[str]
    jbods: Optional[Dict[str, Jbod]]

    class Config:
        fields = {'pk': {'default:': None},}

    class Meta:
        model_key_prefix = 'plant'


Migrator().run()
