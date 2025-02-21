from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated, List

from app.models.movie import Movie
from app.models.booking import Booking
from app.database import get_db
from app.utils.exceptions import BOOKING_NOT_FOUND_ERROR, MOVIE_NOT_FOUND_ERROR, BOOKING_ALREADY_EXISTS_ERROR
from app.utils.dependencies import is_authenticated
from app.schemas.bookingSchema import ViewAllMovies, BookingDone, BookingResponse, BookingCreate

router = APIRouter(
    tags=["user"]
)

@router.get("/movies", response_model=List[ViewAllMovies], status_code=status.HTTP_200_OK)
def get_movies(db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_authenticated)):
    """Retrieve all available movies."""
    return db.query(Movie).all()

@router.post("/movies/{movie_id}/book", response_model=BookingDone, status_code=status.HTTP_201_CREATED)
def book_ticket(request: BookingCreate, db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_authenticated)):
    """Book a ticket for a selected movie."""
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

@router.delete("/movies/{movie_id}/cancel", status_code=status.HTTP_204_NO_CONTENT)
def cancel_booking(movie_id: int, db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_authenticated)):
    """Cancel an existing booking."""
    booking = db.query(Booking).filter(Booking.movie_id == movie_id, Booking.user_id == user.get("id")).first()
    if not booking:
        raise BOOKING_NOT_FOUND_ERROR
    
    db.delete(booking)
    db.commit()
    return {"message": "Booking cancelled successfully"}

@router.get("/movies/history", response_model=List[BookingResponse], status_code=status.HTTP_200_OK)
def get_booking_history(db: Annotated[Session, Depends(get_db)], user: dict = Depends(is_authenticated)):
    """Retrieve all past bookings for the current user."""
    return db.query(Booking).filter(Booking.user_id == user["id"]).all()
