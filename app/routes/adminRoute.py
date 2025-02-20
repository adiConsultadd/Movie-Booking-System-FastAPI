from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from typing import Annotated, List
from app.models.movie import Movie
from app.models.booking import Booking
from app.schemas.movieSchema import MovieCreate, MovieResponse, ViewMovieResponse
from app.utils.exceptions import MOVIE_NOT_FOUND_ERROR, INVALID_MOVIE_DATA
from app.utils.dependencies import is_admin
from app.schemas.bookingSchema import ViewBooking

# Creating Admin Router
router=APIRouter(
    prefix="/admin",
    tags=['admin']
)

# View All Movies
@router.get("/movies",  response_model=List[ViewMovieResponse], status_code=status.HTTP_200_OK)
def get_movies(db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_admin)
):
    movies = db.query(Movie).all()
    return movies

# Add A New Movie
@router.post('/movies', response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def add_movie(request:MovieCreate, db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_admin)
):
    if not request.title or not request.description or not request.showtime:
        return INVALID_MOVIE_DATA
    new_movie = Movie(title=request.title, description=request.description, showtime=request.showtime)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return {"message" : "Movie added successfully", "movie" : new_movie}

# Update An Existing Movie
@router.put('/movies/{id}', response_model=MovieResponse)
def update_movie(id:int, request:MovieCreate, db:Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_admin)
):
    existing_movie = db.query(Movie).filter(Movie.id == id).first()
    if not existing_movie:
        raise MOVIE_NOT_FOUND_ERROR
    
    existing_movie.title = request.title
    existing_movie.description = request.description
    existing_movie.showtime = request.showtime
    db.commit()
    return {"message" : "Movie Updated Successfully", "movie" : existing_movie}

# Delete An Existing Movie
@router.delete('/movies/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id:int, db:Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_admin)
):
    existing_movie = db.query(Movie).filter(Movie.id == id).first()
    if not existing_movie:
        raise MOVIE_NOT_FOUND_ERROR
    db.delete(existing_movie)
    db.commit()
    return {"message": "Movie deleted successfully", "movie":existing_movie}


# View all bookings
@router.get("/bookings", response_model=List[ViewBooking])
def get_bookings(db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_admin)
):
    bookings = db.query(Booking).all()
    return bookings
    