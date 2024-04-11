from database import DbSession
from .models import Teachers
import bcrypt
from typing import Annotated
from fastapi import Cookie
from jose import jwt, JWTError
from config import settings
from .exceptions import get_invalid_token_exception, teacher_exception


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def get_all_teachers(db: DbSession):
    return db.query(Teachers).all


def get_by_email(db: DbSession, email: str):
    return db.query(Teachers).filter(Teachers.email == email).one_or_none()


def get_current_user(db: DbSession, token: Annotated[str | None, Cookie(alias="jwt")] = None):

    if token is None:
        raise get_invalid_token_exception()

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )

        email = payload.get("email")

        if email is None:
            raise get_invalid_token_exception()
        
    
    except JWTError:
        raise get_invalid_token_exception()
    
    user = get_by_email(db, email=email)

    if user is None:
        raise teacher_exception()
    
    return user

