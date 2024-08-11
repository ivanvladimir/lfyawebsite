from fastapi import APIRouter

from app.api.routes import teacher, user, public

api_router = APIRouter()
api_router.include_router(public.router, tags=["public"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
