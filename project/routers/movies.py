from ..schemas import MovieRequestModel
from ..schemas import MovieResponseModel
from ..database import Movie
from fastapi import HTTPException
from fastapi import APIRouter


router = APIRouter(prefix='/movies')


@router.post('', response_model=MovieResponseModel)
async def create_movie(movie: MovieRequestModel):
    movie = Movie.create(
        title = movie.title
    )
    return movie

@router.get('', response_model=MovieResponseModel)
async def create_movie(movie_id:int):
    movie = Movie.select().where(Movie.id == movie_id).first()
    if movie is None:
        raise HTTPException(status_code=404, detail='Movie Not Found')
    return movie