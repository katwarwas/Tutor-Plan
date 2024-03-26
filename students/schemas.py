from fastapi_camelcase import CamelModel
from sqlalchemy import Enum
from datetime import time
from .models import DayEnum, Level
from typing import Optional, List
from fastapi import Request


class BaseStudent(CamelModel):
    name: str
    level: Level
    time: time
    day: DayEnum
    price: int


class CreateStudent(BaseStudent):

    class Config:
        arbitrary_types_allowed = True
        form_atributer=True


class ShowStudents(BaseStudent):
    id: int


class UpdateStudent(CamelModel):
    name: Optional[str]
    level: Optional[Level]
    time: Optional[time]
    day: Optional[DayEnum]
    price: Optional[int]
    



