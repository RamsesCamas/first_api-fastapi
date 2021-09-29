from fastapi import FastAPI
from fastapi.routing import APIRouter

from .database import database as connection
from .database import User
from .database import Movie
from .database import UserReview

from .routers import user_router
from .routers import movie_router
from .routers import review_router


app = FastAPI(title='Proyecto para pelis',
              description='En este proyecto vamos a reseñar peliculas',
              version='1')
api_v1 = APIRouter(prefix='/api/v1')             
api_v1.include_router(user_router)
api_v1.include_router(movie_router)
api_v1.include_router(review_router)

app.include_router(api_v1)
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
    return 'Esta es la sección sobre nosotros, la API de películas'
