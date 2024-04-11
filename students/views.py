from fastapi import APIRouter, Request, Form, Response, Depends
from typing import Annotated
from .schemas import CreateStudent, ShowStudents, UpdateStudent
from database import DbSession
from .services import show_all_students, update, delete, get_student_by_id, price_sum
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette import status
from .models import Students
from .exceptions import student_exception, teacher_authorized_exceptions
from starlette.responses import RedirectResponse
from auth.services import get_current_user
from auth.schemas import Teacher


router = APIRouter(
    tags=["student"],
)

templates = Jinja2Templates(directory="templates")

CurrentUser = Annotated[Teacher, Depends(get_current_user)]

@router.get("/plan",response_model=list[ShowStudents], dependencies=[Depends(get_current_user)])
async def show(request: Request, db: DbSession, current_user: CurrentUser):
    return show_all_students(db_session=db,request=request, id=current_user.id)


@router.get("/student/create", response_class=HTMLResponse, dependencies=[Depends(get_current_user)])
async def create(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.get("/sum")
async def sum(request: Request, db: DbSession):
    return price_sum(db_session=db,request=request)



@router.post("/student/create", dependencies=[Depends(get_current_user)])
async def create_student(db: DbSession, current_user: CurrentUser, request: Request, name: str = Form(...), level: str = Form(...), time: str = Form(...), day: str = Form(...), price: int = Form(...)):
    student = Students()
    student.name = name
    student.level = level 
    student.teacher_id = current_user.id
    student.time = time
    student.day = day
    student.price = price
    db.add(student)
    db.commit()
    db.refresh(student)

    return RedirectResponse(url="/student/create", status_code=status.HTTP_302_FOUND)




@router.get("/student/update/{student_id}", response_class=HTMLResponse,  dependencies=[Depends(get_current_user)])
async def update_S(request: Request, student_id: int, db: DbSession):
    student = get_student_by_id(student_id, db)
    return templates.TemplateResponse("update.html", {"request": request, "student": student})


@router.post("/student/update/{student_id}",  dependencies=[Depends(get_current_user)])
async def update_student(db: DbSession, current_user: CurrentUser, request: Request, student_id: int, name: str = Form(...), level: str = Form(...), time: str = Form(...), day: str = Form(...), price: int = Form(...)):
    student = get_student_by_id(student_id, db)
    
    student.name = name
    student.level = level 
    student.teacher_id = current_user.id
    student.time = time
    student.day = day
    student.price = price
    db.commit()
    db.refresh(student)

    return RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)


@router.patch("/update/{id}", response_model=UpdateStudent)
async def update_student(id:int, db: DbSession, student_in: UpdateStudent):
    return update(db_session=db, id=id, student_in=student_in)


@router.delete("/delete/{id}", dependencies=[Depends(get_current_user)])
async def delete_student(request: Request, current_user: CurrentUser, id: int, db: DbSession):
    student = get_student_by_id(id, db)
    if student.teacher_id != current_user.id:
        raise teacher_authorized_exceptions()
    delete(id=id, db_session=db)
    return Response(status_code=200)

    
