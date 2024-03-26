from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine

from  students import models as students_models
from students.views import router as students_router


students_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    'http://localhost:3000'

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins
)

app.include_router(students_router)

app.mount("/static", StaticFiles(directory="static"), name="static")
