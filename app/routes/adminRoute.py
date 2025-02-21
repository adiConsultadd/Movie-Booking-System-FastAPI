from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.database import get_db
from app.models.movie import Movie
from app.models.booking import Booking
from app.schemas.movieSchema import MovieCreate, MovieResponse, ViewMovieResponse
from app.schemas.bookingSchema import ViewBooking
from app.utils.exceptions import MOVIE_NOT_FOUND_ERROR, INVALID_MOVIE_DATA
from app.utils.dependencies import is_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)

@router.get("/movies", response_model=List[ViewMovieResponse], status_code=status.HTTP_200_OK)
def get_movies(db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_admin)):
    """Retrieve a list of all movies available in the database."""
    return db.query(Movie).all()

@router.post("/movies", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
def add_movie(request: MovieCreate, db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_admin)):
    """Add a new movie to the database."""
    if not request.title or not request.description or not request.showtime:
        return INVALID_MOVIE_DATA
    new_movie = Movie(title=request.title, description=request.description, showtime=request.showtime)
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    return {"message": "Movie added successfully", "movie": new_movie}

@router.put("/movies/{id}", response_model=MovieResponse)
def update_movie(id: int, request: MovieCreate, db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_admin)):
    """Update an existing movie's details by its ID."""
    existing_movie = db.query(Movie).filter(Movie.id == id).first()
    if not existing_movie:
        raise MOVIE_NOT_FOUND_ERROR
    
    existing_movie.title = request.title
    existing_movie.description = request.description
    existing_movie.showtime = request.showtime
    db.commit()
    return {"message": "Movie Updated Successfully", "movie": existing_movie}

@router.delete("/movies/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id: int, db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_admin)):
    """Delete a movie from the database by its ID."""
    existing_movie = db.query(Movie).filter(Movie.id == id).first()
    if not existing_movie:
        raise MOVIE_NOT_FOUND_ERROR
    db.delete(existing_movie)
    db.commit()
    return {"message": "Movie deleted successfully", "movie": existing_movie}

@router.get("/bookings", response_model=List[ViewBooking])
def get_bookings(db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_admin)):
    """Retrieve a list of all movie bookings."""
    return db.query(Booking).all()
