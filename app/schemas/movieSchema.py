from pydantic import BaseModel


class ViewMovieResponse(BaseModel):
    title: str
    description: str
    showtime: str

    class Config:
        from_attributes = True


class MovieCreate(BaseModel):
    title: str
    description: str
    showtime: str


class MovieResponse(BaseModel):
    message: str
    movie: MovieCreate
