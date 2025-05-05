from fastapi import FastAPI, HTTPException, Depends, UploadFile
import models
import PYD
from database import get_db
from typing import List
from sqlalchemy.orm import Session
import shutil
from datetime import datetime
import time
from fastapi.staticfiles import StaticFiles
from auth import basic_auth
import re

app = FastAPI()

app.mount("/files", StaticFiles(directory='files'), name="files")

@app.get("/movies", response_model=List[PYD.SchemeMovie])
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(models.Movie).all()
    return movies

@app.get("/movies/{id}", response_model=PYD.SchemeMovie)
def get_movie(id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(404, detail="Фильм не найден")
    return movie

@app.post("/movies", response_model=PYD.SchemeMovie)
def create_movie(Movie: PYD.CreateMovie, db: Session = Depends(get_db), user: models.User = Depends(basic_auth)):
    genres = db.query(models.Genre).filter(models.Genre.id.in_(Movie.genre_ids)).all()
    if len(genres) != len(Movie.genre_ids):
        raise HTTPException(404, detail="Некоторые жанры не найдены")
    movie = models.Movie(
        title=Movie.title,
        year=Movie.year,
        duration=Movie.duration,
        rating=Movie.rating,
        description=Movie.description,
        poster_url=None,
        date_added=datetime.utcnow()
    )
    movie.genres = genres
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie

@app.put("/movies/{id}", response_model=PYD.SchemeMovie)
def update_movie(
    id: int,
    movie_update: PYD.UpdateMovie,
    db: Session = Depends(get_db),
    user: models.User = Depends(basic_auth),
):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(404, detail="Фильм не найден")
    for var, value in movie_update.dict(exclude_unset=True).items():
        if var == "genre_ids" and value is not None:
            genres = db.query(models.Genre).filter(models.Genre.id.in_(value)).all()
            if len(genres) != len(value):
                raise HTTPException(404, detail="Некоторые жанры не найдены")
            movie.genres = genres
        elif hasattr(movie, var):
            setattr(movie, var, value)
    db.commit()
    db.refresh(movie)
    return movie

@app.put("/movies/{id}/image", response_model=PYD.SchemeMovie)
def update_movie_poster(id: int, image: UploadFile, db: Session = Depends(get_db), user: models.User = Depends(basic_auth)):
    movie_db = (
        db.query(models.Movie).filter(models.Movie.id == id).first()
    )
    if not movie_db:
        raise HTTPException(404, detail="Фильм не найден")
    if image.content_type not in ("image/png", "image/jpeg"):
        raise HTTPException(400, detail="Неверный тип файла")
    contents = image.file.read()
    max_size = 2 * 1024 * 1024
    if len(contents) > max_size:
        raise HTTPException(400, detail="Размер файла превышает 2MB")
    filename = f"{int(time.time())}_{image.filename}"
    with open(f"files/{filename}", "wb") as f:
        image.file.seek(0)
        shutil.copyfileobj(image.file, f)
    movie_db.poster_url = f"http://127.0.0.1:8000/files/{filename}"
    db.commit()
    db.refresh(movie_db)
    return movie_db

@app.delete("/movies/{id}")
def delete_movie(id: int, db: Session = Depends(get_db), user: models.User = Depends(basic_auth)):
    movie = db.query(models.Movie).filter(models.Movie.id == id).first()
    if not movie:
        raise HTTPException(404, detail="Фильм не найден")
    db.delete(movie)
    db.commit()
    return {"detail": "Фильм удален"}

@app.get("/genres", response_model=List[PYD.BaseGenre])
def get_genres(db: Session = Depends(get_db)):
    return db.query(models.Genre).all()

@app.post("/genres", response_model=PYD.BaseGenre)
def create_genre(genre: PYD.CreateGenre, db: Session = Depends(get_db), user: models.User = Depends(basic_auth)):
    existing = db.query(models.Genre).filter(models.Genre.name == genre.name).first()
    if existing:
        raise HTTPException(400, detail="Жанр с таким именем уже существует")
    new_genre = models.Genre(name=genre.name, description=genre.description)
    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)
    return new_genre

@app.post("/user", response_model=PYD.BaseUser)
def user_reg(create_user: PYD.CreateUser, db: Session = Depends(get_db)):
    user_db = db.query(models.User).filter(models.User.username == create_user.username).first()
    if user_db:
        raise HTTPException(400, "Логин занят")
    if not re.match(r'^[A-Za-z0-9]{4,}$', create_user.username):
        raise HTTPException(400, "Логин должен содержать минимум 4 символа и состоять из букв и цифр")
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, create_user.email):
        raise HTTPException(400, "Неккоректный формат email")
    if len(create_user.password) < 8:
        raise HTTPException(400, "Пароль должен быть не менее 8 символов")
    if not re.search(r'[A-Za-z]', create_user.password) or not re.search(r'[0-9]', create_user.password):
        raise HTTPException(400, "Пароль должен содержать буквы и цифры")
    user_db = models.User()
    user_db.username = create_user.username
    user_db.passwrod = create_user.password
    user_db.email = create_user.email
    db.add(user_db)
    db.commit()
    return user_db