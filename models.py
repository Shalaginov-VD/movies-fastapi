from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

movie_genres = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)

class Genre(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255), nullable=True)

    movies = relationship("Movie", secondary=movie_genres, back_populates="genres")


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=True)
    duration = Column(Integer, nullable=True)
    rating = Column(Float, nullable=True)
    description = Column(String(1000), nullable=True)
    poster_url = Column(String(255))
    date_added = Column(DateTime, default=datetime.utcnow)

    genres = relationship("Genre", secondary=movie_genres, back_populates="movies")
