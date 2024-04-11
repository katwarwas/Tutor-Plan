from .models import Students
from .schemas import CreateStudent, UpdateStudent
from database import DbSession
from .exceptions import student_exception
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy import case, func
from starlette.responses import RedirectResponse 
from starlette import status
from auth.schemas import BaseTeacher


templates = Jinja2Templates(directory="templates")


def show_all_students(db_session: DbSession, request: Request, id: int):
    day_order = {
        "Poniedziałek": 1,
        "Wtorek": 2,
        "Środa": 3,
        "Czwartek": 4,
        "Piątek": 5
    }
    sort_logic = case(day_order, value=Students.day).label("day")
    students = db_session.query(Students).filter(Students.teacher_id == id).order_by(sort_logic).order_by(Students.time).all()
    total_price = db_session.query(func.sum(Students.price)).filter(Students.teacher_id == id).scalar()
    if total_price is None:
        total_price = 0
    return templates.TemplateResponse("students.html", {"request": request, "students": students, "days": day_order, "total": total_price})


def price_sum(db_session: DbSession, request: Request):
    total_price = db_session.query(func.sum(Students.price)).scalar()
    return total_price
    


def get_student_by_id(id, db_session: DbSession):
    return db_session.query(Students).filter(Students.id == id).one_or_none()


def update(*, db_session: DbSession, id: int, student_in:CreateStudent) -> Students:
    student = get_student_by_id(id, db_session=db_session)

    if student is None:
     raise student_exception()

    update_data = student_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db_session.commit()
    db_session.refresh(student)

    return student 
    

def delete(*, id: int, db_session: DbSession):
    student = get_student_by_id(id, db_session=db_session)

    if student is None:
        raise student_exception()

    db_session.delete(student)
    db_session.commit()
    return db_session.query(func.sum(Students.price)).scalar()





