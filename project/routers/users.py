from typing import List
from ..schemas import ReviewResponseModel, UserRequestModel
from ..schemas import UserResponseModel
from ..database import User

from fastapi import HTTPException
from fastapi import APIRouter
from fastapi.security import HTTPBasicCredentials
from fastapi import Response
from fastapi import Cookie

router = APIRouter(prefix='/users')

@router.post('',response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409,'Ese username ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password
    )
    return user
@router.get('',response_model=UserResponseModel)
async def get_user(user_id:int):
    user = User.select().where(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return user

@router.post('/login',response_model=UserResponseModel)
async def login(credentials: HTTPBasicCredentials, response:Response):
    user = User.select().where(User.username == credentials.username).first()
    if user is None:
        raise HTTPException(404, 'User Not Found')
    if user.password != User.create_password(credentials.password):
        raise HTTPException(404, 'Password error')
    response.set_cookie(key='user_id',value=user.id)
    return user

@router.get('/reviews',response_model=List[ReviewResponseModel])
async def get_reviews(user_id: int = Cookie(None)):
    user = User.select().where(User.id == user_id).first()
    if user is None:
        raise HTTPException(404, 'User Not Found')
    return [user_review for user_review in user.reviews]