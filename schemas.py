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

class ReviewValidator():
    @validator('username')
    def username_validator(cls,username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError('El nombre de usuario debe tener más de 3 caracteres y menos de 50')
        return username
class ResponseModel(BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class UserRequestModel(BaseModel):
    username: str
    password: str

    


class UserResponseModel(ResponseModel):
    id: int
    username: str



class MovieRequestModel(BaseModel):
    title: str


class MovieResponseModel(ResponseModel):
    id: int
    title: str
    

class ReviewRequestModel(BaseModel,ReviewValidator):
    user_id : int
    movie_id: int
    review: str
    score: int
class ReviewResponseModel(ResponseModel):
    id: int
    movie: MovieResponseModel
    review: str
    score: int

class ReviewRequestPutModel(BaseModel, ReviewValidator):
    review: str
    score: int