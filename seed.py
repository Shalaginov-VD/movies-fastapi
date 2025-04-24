import models
from database import engine, SessionLocal
from datetime import datetime

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    genre1 = models.Genre(name="Драма", description="Драматические фильмы")
    genre2 = models.Genre(name="Комедия", description="Веселые фильмы")
    genre3 = models.Genre(name="Боевик", description="Экшен и боевые сцены")
    session.add_all([genre1, genre2, genre3])
    session.commit()

    movie1 = models.Movie(
        title="1+1",
        year=2011,
        duration=112,
        rating=8.9,
        description="Прикованный к инвалидному креслу аристократ нанимает себе в помощники человека, который подходит для этой работы меньше всего.",
        poster_url=None,
        genres=[genre1, genre2],
        date_added=datetime.utcnow()
    )
    movie2 = models.Movie(
        title="Такси",
        year=1998,
        duration=89,
        rating=8.0,
        description="Таксист Даниэль помешан на быстрой езде.",
        poster_url=None,
        genres=[genre3],
        date_added=datetime.utcnow()
    )
    session.add_all([movie1, movie2])
    session.commit()
