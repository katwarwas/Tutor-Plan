from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse



main = APIRouter(
    tags=["student"],
)

templates = Jinja2Templates(directory="templates")


@main.get("/", response_class=HTMLResponse)
async def create(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})