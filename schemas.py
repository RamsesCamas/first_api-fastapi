from pydantic import BaseModel

class UserBaseModel(BaseModel):
    username: str
    password: str

class MovieBaseModel(BaseModel):
    title: str