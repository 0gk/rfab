from typing import Optional, Dict
from pydantic import BaseModel


class Three(BaseModel):
    v: int


class Two(BaseModel):
    v: int
    d: Optional[Dict[str, Three]]


class One(BaseModel):
    v: int
    d: Optional[Dict[str, Two]]


one = One(v=1, d={})

one.d['1']=Two(v=2, d={1: Three(v=3), 2: Three(v=33), 3: Three(v=333)})
one.d['2']=Two(v=2, d={1: Three(v=3), 2: Three(v=33), 3: Three(v=333)})

two = One(v=2, d={})
two.d['1']=Two(v=22, d={1: Three(v=23), 2: Three(v=233), 3: Three(v=2333)})

print('-----')
print(one)
print('-----')
print(two)
print('-----')

three = one.copy(deep=True, update=two.dict())

print('======')
print(three)



