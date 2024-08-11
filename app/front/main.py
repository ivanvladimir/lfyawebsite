from fastapi import FastAPI

from app.front.routes import login, teacher

front_app = FastAPI()

front_app.include_router(login.router, tags=["login"])
front_app.include_router(teacher.router, prefix="/teacher",tags=["teacher"])

