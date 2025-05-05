from .basemodels import *

class SchemeMovie(BaseMovie):
    genres: List[BaseGenre] = []