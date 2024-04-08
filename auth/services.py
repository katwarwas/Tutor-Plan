from database import DbSession
from .models import Teachers
import bcrypt


def hash_password(password: str):
    pw = bytes(password, "utf-8")
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pw, salt)


def get_all_teachers(db: DbSession):
    return db.query(Teachers).all

def get_by_email(db: DbSession, email: str):
    return db.query(Teachers).filter(Teachers.email == email).one_or_none()