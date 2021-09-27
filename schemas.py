from peewee import ModelSelect
from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict
from typing import Any 

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj,key,default)
        if isinstance(res,ModelSelect):
            return list(res)
        return res 


class UserRequestModel(BaseModel):
    username: str
    password: str

    @validator('username')
    def username_validator(cls,username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('El nombre de usuario debe tener más de 3 caracteres y menos de 50')
        return username

class UserResponseModel(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class MovieBaseModel(BaseModel):
    title: str