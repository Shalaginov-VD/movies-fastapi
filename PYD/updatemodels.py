from pydantic import BaseModel, Field
from typing import List

class UpdateMovie(BaseModel):
    title: str = Field(min_length=2, max_length=100, example="Титаник")
    genre_ids: List[int]
    year: int = Field(example=2000)
    duration: int = Field(example=90)
    rating: float = Field(ge=0, le=10, example=10)
    description: str = Field(min_length=10, max_length=1000, example="В первом и последнем плавании шикарного Титаника встречаются двое.")