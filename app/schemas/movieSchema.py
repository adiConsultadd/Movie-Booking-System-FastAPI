from pydantic import BaseModel
from datetime import datetime

class ViewMovieResponse(BaseModel):
    title: str
    description: str
    showtime: str

    class Config:
        from_attributes = True


class MovieCreate(BaseModel):
    title: str
    description: str
    showtime: datetime


class MovieResponse(BaseModel):
    message: str
    movie: MovieCreate
