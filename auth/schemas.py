from fastapi_camelcase import CamelModel
from .services import hash_password
from pydantic import field_validator
from pydantic import BaseModel

class BaseTeacher(CamelModel):
    id: int
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

class Teacher(BaseModel):
    email: str