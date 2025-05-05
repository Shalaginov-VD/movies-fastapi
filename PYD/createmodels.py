from pydantic import BaseModel, Field, EmailStr
from typing import List

class CreateMovie(BaseModel):
    title: str = Field(min_length=2, max_length=100, example="Титаник")
    genre_ids: List[int] = []
    year: int = Field(example=2000)
    duration: int = Field(example=90)
    rating: float = Field(ge=0, le=10, example=10)
    description: str = Field(min_length=10, max_length=1000, example="В первом и последнем плавании шикарного Титаника встречаются двое.")

class CreateGenre(BaseModel):
    name: str = Field(example="Драма")
    description: str = Field(None, example="Драматические фильмы")

class CreateUser(BaseModel):
    username: str = Field(example="Denis123", min_length=3, max_length=60)
    password: str = Field(example="qwerty123", min_length=8, max_length=60)
    email: EmailStr | None = Field(None)