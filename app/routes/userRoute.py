from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List
from app.models.movie import Movie
from app.models.booking import Booking
from app.database import get_db
from app.utils.exceptions import BOOKING_NOT_FOUND_ERROR, MOVIE_NOT_FOUND_ERROR, BOOKING_ALREADY_EXISTS_ERROR
from app.utils.dependencies import is_authenticated
from app.schemas.bookingSchema import ViewAllMovies
from app.schemas.bookingSchema import BookingDone, BookingResponse, BookingCreate

# Creating User Router
router=APIRouter(
    tags=['user']
)

# View All Available Movies
@router.get("/movies", response_model=List[ViewAllMovies], status_code=status.HTTP_200_OK)
def get_movies(db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_authenticated)
):
    movies = db.query(Movie).all()
    return movies

# Book A New Ticket
@router.post("/movies/{movie_id}/book",response_model=BookingDone, status_code=status.HTTP_201_CREATED)
def book_ticket(request:BookingCreate , db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_authenticated)
):
    movie = db.query(Movie).filter(Movie.id == request.movie_id).first()
    
    if not movie:
        raise MOVIE_NOT_FOUND_ERROR

    existing_booking = db.query(Booking).filter(Booking.movie_id == request.movie_id, Booking.user_id == user["id"]).first()
    if existing_booking:
        raise BOOKING_ALREADY_EXISTS_ERROR

    booking = Booking(user_id=user["id"], movie_id=request.movie_id)
    db.add(booking)
    db.commit()
    db.refresh(booking)
    
    return {"message": "Ticket booked successfully", "booking": booking}

# Cancel An Exiting booking
@router.delete("/movies/{movie_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(movie_id: int, db:Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_authenticated)
):
    booking = db.query(Booking).filter(Booking.movie_id==movie_id, Booking.user_id==user.get("id")).first()
    
    if not booking:
        raise BOOKING_NOT_FOUND_ERROR

    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully"}

# View All Bookings For The Current User
@router.get("/movies/history", response_model=List[BookingResponse], status_code=status.HTTP_200_OK)
def get_booking_history(db: Annotated[Session, Depends(get_db)],
    user: dict = Depends(is_authenticated)
):
    bookings = db.query(Booking).filter(Booking.user_id == user["id"]).all()
    return bookings

