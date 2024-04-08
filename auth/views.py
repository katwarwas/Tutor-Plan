from fastapi import APIRouter, Request, Response, Form
from database import DbSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .services import hash_password, get_by_email
from .models import Teachers


admin = APIRouter(
    tags=["Admin"]
)

templates = Jinja2Templates(directory="templates")


@admin.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@admin.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, db: DbSession, name: str = Form(...), email: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    if get_by_email(db, email) is not None:
        return """<div id="info">Użytkownik o tym e-mailu już istnieje! Użyj innego e-maila.</div>"""
    
    if password != confirm_password:
        return """<div id="info">Hasła nie są zgodne</div>"""
    
    teacher = Teachers()
    hashed_password = hash_password(password)

    teacher.name = name
    teacher.email = email
    teacher.password = hashed_password

    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    return """<div id="info">Zarejestrowano pomyślnie</div>"""


