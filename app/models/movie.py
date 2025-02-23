from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    showtime = Column(DateTime)
