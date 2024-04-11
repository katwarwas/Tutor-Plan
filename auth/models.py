from sqlalchemy import Column, Integer, String, LargeBinary
from database import Base
import bcrypt
from config import settings
from jose import jwt
from datetime import datetime, timedelta

class Teachers(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(LargeBinary, nullable=False)

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password)
    
    @property
    def token(self):
        exp = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    
    @property
    def refresh_token(self):
        exp = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_hours)
        data = {
            "exp": exp,
            "email": self.email,
        }
        return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)
    