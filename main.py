from fastapi import FastAPI
from fastapi import HTTPException
from database import database as connection

from database import User
from database import Movie
from database import UserReview

from schemas import UserRequestModel
from schemas import UserResponseModel

from schemas import ReviewRequestModel
from schemas import ReviewResponseModel
from schemas import ReviewRequestPutModel

from schemas import MovieRequestModel
from schemas import MovieResponseModel

from typing import List



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
    return 'Esta es la sección sobre nosotros, la API de películas'

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

@app.post('/movies', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    movie = Movie.create(
        title = movie.title
    )
    return movie

@app.post('/reviews',response_model=ReviewResponseModel)
async def create_review(user_review: ReviewRequestModel):

    if User.select().where(User.id == user_review.user_id).first() is None:
        raise HTTPException(status_code=404, detail='User Not Found')

    if Movie.select().where(Movie.id == user_review.movie_id).first() is None:
        return HTTPException(status_code=404,detail='Movie Not Found')
    user_review = UserReview.create(
        user_id=user_review.user_id,
        movie_id=user_review.movie_id,
        review=user_review.review,
        score=user_review.score
    )
    return user_review

@app.get('/reviews', response_model=List[ReviewResponseModel])
async def get_reviews():
    reviews = UserReview.select()
    my_reviews = [{'id': user_re.id,'movie_id':user_re.movie_id,'review':user_re.reviews,'score':user_re.score}  for user_re in reviews]
    return  my_reviews

@app.get('/reviews/{review_id}', response_model=ReviewResponseModel)
async def get_review(review_id:int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404,detail='Review Not Found')
    return {'id': user_review.id,'movie_id':user_review.movie_id,'review':user_review.reviews,'score':user_review.score}


@app.put('/reviews/{review_id}',response_model=ReviewResponseModel)
async def update_review(review_id:int,review_request: ReviewRequestPutModel):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404,detail='Review Not Found')
    
    user_review.review = review_request.review
    user_review.score = review_request.score
    user_review.save()
    return user_review

@app.delete('/reviews/{review_id}',response_model=ReviewResponseModel)
async def delete_review(review_id:int):
    user_review = UserReview.select().where(UserReview.id == review_id).first()
    if user_review is None:
        raise HTTPException(status_code=404,detail='Review Not Found')
    user_review.delete_instance()

    return {'id': user_review.id,'movie_id':user_review.movie_id,'review':user_review.reviews,'score':user_review.score}