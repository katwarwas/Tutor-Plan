from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine
from auth import models as auth_models
from auth.views import admin as auth_router
from basic.views import main as main_router
from  students import models as students_models
from students.views import router as students_router


auth_models.Base.metadata.create_all(bind=engine)
students_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

app.include_router(auth_router)
app.include_router(main_router)
app.include_router(students_router)


app.mount("/static", StaticFiles(directory="static"), name="static")
