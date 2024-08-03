import time
from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core.config import settings
#from app.core.security import get_password_hash
from app.models import Token, UserEnum

templates = Jinja2Templates(directory="app/front/templates")

router = APIRouter()

@router.get("/")
async def teacher_home(request:Request, current_user: CurrentUser) -> HTMLResponse:
    """
    Main view for teacher
    """
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    if current_user.role is UserEnum.teacher:
        groups = await crud.get_groups_teacher(current_user)
        groups.sort(key=lambda g: g.created, reverse = True)
        response=templates.TemplateResponse(
            request=request, 
            name="teacher/home.html", 
            context={
                "current_user":current_user,
                "groups":groups,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"}
        )
        return response
    else:
        raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/{course_id}/list")
async def list_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        students,course = await crud.get_students_from_course(course_id) 
        students = sorted(students, key=lambda s: s[0].firstname)
        response=templates.TemplateResponse(
            request=request,
            name="teacher/list.html",
            context={
                "current_user":current_user,
                "students":students,
                "course_id":course_id,
                "course_id_":course.id,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"
            }
        )
        return response
    return "401", "Not authorized"


@router.get("/{course_id}/attendance/list")
async def attendance_list_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        if not current_user.role == UserEnum.teacher:
            return "401", "Not authorized"

        form = DateF()
        course = courses.find_one_by({"course_id": course_id})
        days = attendance.find_by({"course": str(course.id)})
        days = set(d.date for d in days)
        days = [(d,humanize.naturaldate(d)) for d in sorted(days,reverse=True)]

        return render_template(
            "teacher/attendance_list.html",
            days=days,
            form=form,
            course_id=course_id,
            course_id_=course.id,
            elapsed_time_seconds=f"{elapsed_time():2.3f}",
        )
    return "401", "Not authorized"

