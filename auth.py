from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
import models as m

security = HTTPBasic()


def basic_auth(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user_db = db.query(m.User).filter(m.User.username == credentials.username).first()
    if not user_db:
        raise HTTPException(404, "Пользователь не найден")
    if user_db.passwrod == credentials.password:
        return user_db
    raise HTTPException(401, "Неверный логин или пароль")
