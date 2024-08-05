import time
import datetime
import humanize
from typing import Annotated, Any

from fastapi import APIRouter, Request, HTTPException

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core import uptime
from app.core.config import settings
from app.models import Token, UserEnum

router = APIRouter()

@router.get("/add/{course_student_id}")
async def add_participation_teacher(course_student_id: str, request:Request, current_user: CurrentUser) -> Any:
    """
    Add a point for participation
    """
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    if current_user.role is UserEnum.teacher:
        course_student = await crud.get_course_student(course_student_id)
        course_student_ = { 
            'participation':course_student['participation']+1,
            'modified':datetime.datetime.utcnow()
        }
        await crud.update_course_student(course_student['_id'],course_student_)
        return f"<strong>{int(course_student_['participation'])}</strong>"
    else:
        raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/substract/{course_student_id}")
async def substract_participation_teacher(course_student_id: str, request:Request, current_user: CurrentUser) -> Any:
    """
    Substract a point for participation
    """
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    if current_user.role is UserEnum.teacher:
        course_student = await crud.get_course_student(course_student_id)
        course_student_ = { 
            'participation':course_student['participation']-1,
            'modified':datetime.datetime.utcnow()
        }
        await crud.update_course_student(course_student['_id'],course_student_)
        return f"<strong>{int(course_student_['participation'])}</strong>"
    else:
        raise HTTPException(status_code=401, detail="Not authorized")


