from pydantic import BaseModel, Field, HttpUrl, EmailStr
from datetime import datetime
from typing import List, Optional

class BaseGenre(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(example="Драма")
    description: str = Field(None, example="Драматические фильмы")

class BaseMovie(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=2, max_length=100, example="Титаник")
    genres: List[BaseGenre] = []
    year: int = Field(example=2000)
    duration: int = Field(example=90)
    rating: float = Field(ge=0, le=10, example=10)
    description: str = Field(min_length=10, max_length=1000, example="В первом и последнем плавании шикарного Титаника встречаются двое.")
    poster_url: Optional[str] = None
    date_added: datetime

class BaseUser(BaseModel):
    id: int
    username: str = Field(example="Denis123")
    email: EmailStr | None = Field(None, example="test@mail.ru")