import time
import datetime
import humanize
from typing import Annotated, Any

from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core import uptime
from app.core.config import settings
from app.models import Token, UserEnum, Attendance, AttendanceEnum

router = APIRouter()

@router.get("/add/{course_student_id}")
async def add_participation_teacher(course_student_id: str, request:Request, current_user: CurrentUser) -> str:
    """
    Add a point for participation
    """
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
async def substract_participation_teacher(course_student_id: str, request:Request, current_user: CurrentUser) -> str:
    """
    Substract a point for participation
    """
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

@router.post("/attendance/create/{course_id}")
async def attendance_create_teacher(course_id: str, date: Annotated[str, Form()], request:Request, current_user: CurrentUser, response_class=HTMLResponse) -> HTMLResponse:
    """
    Create attendance for a class
    """
    if current_user.role is UserEnum.teacher:
        #if await crud.exists_date_course(course_id=course_id,date=date):
        #    raise HTTPException(status_code=403, detail="Date already exists")
        students,course = await crud.get_students_from_course(str(course_id))
        
        atts =[]
        for s,_,_ in students:
            gt = datetime.datetime.utcnow()
            att = Attendance(
                student=str(s.id),
                course=str(course.id),
                date=datetime.datetime.strptime(date, "%d/%m/%Y"),
                status=AttendanceEnum.present,
                created=gt,
                modified=gt,
            )
            atts.append(att)
        msg= f"<li hx-swap-oob='true'><a href='/class/teacher/{course_id}/attendance/modify/{date.replace('/','-')}%2000:00:00'>{date}</a></li>"
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")




