from typing import Optional, Dict 
from enum import Enum

from pydantic import BaseModel, ConfigDict, constr

from rdb import r

#redis = get_redis_connection(
#    host = s.REIDS_HOST,
#    port = s.REIDS_PORT,
#    #password='lksjdflkmsaclkasuoirwjaoifdewu798432u09ei3domsadr8=====>jflsamfoiweuyrosiajowau82098570',
#    #decode_responses=True,
#)

class PyBaseModel(BaseModel):
    pass

# = STATE =============================================

class Slot(PyBaseModel):

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


class Jbod(PyBaseModel):

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


class Plant(PyBaseModel):
    name: Optional[str]
    testoptions: Dict[int, str]
    chosentest: int
    jbods: Optional[Dict[str, Jbod]]

