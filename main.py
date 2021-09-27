from fastapi import FastAPI
from fastapi import HTTPException
from database import database as connection

from database import User
from database import Movie
from database import UserReview

from schemas import UserRequestModel
from schemas import UserResponseModel



app = FastAPI(title='Proyecto para pelis',
              description='En este proyecto vamos a reseñar peliculas',
              version='1')

#Se ejecutará antes de iniciar el servidor
@app.on_event('startup')
def startup():
    if connection.is_closed():
        connection.connect()
    #Si las tablas ya existen no va a pasar nada
    connection.create_tables([User,Movie,UserReview])

#Se ejecutará cuando el servidor esté finalizando
@app.on_event('shutdown')
def shutdown():
    if not connection.is_closed():
        connection.close()
        print('Closing Database')

@app.get('/')
async def home():
    return 'Hola Mundo desde un server en Fast API'

@app.get('/about')
async def about():
    return 'About Us'

@app.post('/user',response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        return HTTPException(409,'Ese username ya existe')

    hash_password = User.create_password(user.password)
    user = User.create(
        username = user.username,
        password = hash_password
    )
    return user