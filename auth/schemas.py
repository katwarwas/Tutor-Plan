from fastapi_camelcase import CamelModel
from sqlalchemy import Enum
from datetime import time
from .models import DayEnum, Level
from typing import Optional, List
from fastapi import Request
from .services import hash_password
from pydantic import field_validator


class BaseTeacher(CamelModel):
    name: str
    email: str
    password: str


class CreateStudent(BaseTeacher):

    @field_validator("password")
    def password_required(cls, password):
        return hash_password(password)
    
    class Config:
        arbitrary_types_allowed = True
        form_atributer=True