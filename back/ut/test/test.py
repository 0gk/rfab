from typing import Optional, Dict
from pydantic import BaseModel
from redis_om import get_redis_connection, EmbeddedJsonModel, JsonModel, Field, Migrator


class One(JsonModel):
    a: int
    b: int


class Two(One):
    a: int
    b: str 

a = One(a=1, b=2)
b = Two(a=1, b='two')
print(a, b)


