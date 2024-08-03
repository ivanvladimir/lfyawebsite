from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.front.routes import login, teacher

front_app = FastAPI()

front_app.mount("/static", StaticFiles(directory="app/front/static"), name="static")

front_app.include_router(login.router, tags=["login"])
front_app.include_router(teacher.router, prefix="/teacher",tags=["teacher"])

