from pydantic import BaseModel
from typing import Optional

class ViewBooking(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True  

class BookingCreate(BaseModel):
    movie_id: int

class BookingResponse(BaseModel):
    user_id: int
    movie_id: int

    class Config:
        from_attributes = True

class ViewAllMovies(BaseModel):
    title : str
    showtime : str

class BookingDone(BaseModel):
    message:str
    booking:BookingResponse
