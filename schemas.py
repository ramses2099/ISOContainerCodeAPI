from typing import Optional
from pydantic import BaseModel

class ISOContainerTypeBase(BaseModel):
    gkey: int
    code:str
    description:str
    length:int 
    height:float
    group:str


class ISOContainerTypeSearch(BaseModel):
    gkey:Optional[int] = None
    code:Optional[str] = None

class ISOContainerTypeCreate(BaseModel):
    code:str
    description:str
    length:int 
    height:float
    group:str

class ISOContainerTypeUpdate(BaseModel):
    gkey: int
    code:str
    description:str
    length:int 
    height:float
    group:str

