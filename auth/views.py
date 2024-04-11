from fastapi import APIRouter, Request, Response, Form, Depends
from database import DbSession
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .services import hash_password, get_by_email
from .models import Teachers
from starlette.responses import RedirectResponse
from starlette import status
from config import settings
from .services import get_current_user


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


@admin.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@admin.post("/login", response_class=HTMLResponse)
async def login_user(db: DbSession, email:str = Form(...), password: str = Form(...)):
    user_data = Teachers()
    user_data.email = email
    user_data.password = password
    user = get_by_email(db, user_data.email)

    if not user or not user.check_password(user_data.password):
        return """<div><p>Blędne hasło lub email.</p></div>""" 
    
    
    redirect = RedirectResponse(url="/plan", status_code=status.HTTP_302_FOUND)

    redirect.set_cookie(
        key="jwt",
        value=user.refresh_token,
        httponly=True,
        secure=True,
        samesite=None,
        max_age=60 * 60 * settings.refresh_token_expire_hours,
    )

    return redirect



@admin.get("/logout", dependencies=[Depends(get_current_user)])
async def logout(response: Response, request: Request):
    redirect = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    redirect.delete_cookie(key="jwt")
    return redirect

