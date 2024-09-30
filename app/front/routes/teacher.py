import time
from datetime import timedelta
from typing import Annotated, Any
import humanize
import markdown
import os

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app import crud
from app.api.deps import CurrentUser
from app.front.forms import DateF, UserF, AssigmentF
from app.core import security
from app.core.config import settings
#from app.core.security import get_password_hash
from app.models import Token, UserEnum

templates = Jinja2Templates(directory="app/front/templates")

router = APIRouter()

@router.get("/")
async def home_teacher(request:Request, current_user: CurrentUser) -> HTMLResponse:
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

@router.get("/page/{view}")
async def page_teacher(view: str, request:Request, current_user: CurrentUser) -> HTMLResponse:
    """
    Main view for pages
    """
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    content_path="app/content/"

    if os.path.exists(os.path.join(content_path,f"{view}.md")):
        content = open(os.path.join(content_path,f"{view}.md")).read()
        md = markdown.Markdown(extensions=['meta','tables'])
        content= md.convert(content)
        response=templates.TemplateResponse(
            request=request, 
            name="teacher/page.html", 
            context={
                "current_user":current_user,
                "content":content,
                "metadata":md.Meta,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"})        
        return response
    else:
        raise HTTPException(status_code=404, detail="Page not found")

@router.get("/{course_id}/list")
async def list_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        students,course = await crud.get_students_from_course(course_id) 
        students = [s for s in students if s[0].active]
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


@router.get("/{course_id}/attendance")
async def attendance_list_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        form = DateF(request)
        dates, course = await crud.get_unique_dates_attendance_course(course_id)
        days = [(d,humanize.naturaldate(d)) for d in sorted(dates,reverse=True)]

        response=templates.TemplateResponse(
            request=request,
            name="teacher/attendance.html",
            context= {
                "days":days,
                "form":form,
                "course_id":course_id,
                "course_id_":course.id,
                "current_user":current_user,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"}
        )
        return response
    return "401", "Not authorized"

@router.get("/{course_id}/attendance/modify/{date}")
async def attendance_modify_teacher(course_id:str, date:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:

        students, course = await crud.get_students_from_course_date(course_id,date)
        students = [s for s in students if s[0].active]

        response=templates.TemplateResponse(
            request=request,
            name="teacher/attendance_modify.html",
            context= {
                "date":date,
                "students":students,
                "course_id":course_id,
                "course_id_":course.id,
                "current_user":current_user,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"}
        )
        return response
    return "401", "Not authorized"

@router.get("/{course_id}/assigment/list/{name}")
async def assigment_list_teacher(course_id:str, name:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:

        students, course = await crud.get_students_from_course_assigment(course_id,name)
        students = [s for s in students if s[0].active]
        print(students[0])

        response=templates.TemplateResponse(
            request=request,
            name="teacher/assigment_list.html",
            context= {
                "name":name,
                "students":students,
                "sections": students[0][1].sections,
                "course_id":course_id,
                "course_id_":course.id,
                "current_user":current_user,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"}
        )
        return response
    return "401", "Not authorized"



@router.get("/{course_id}/assigment")
async def assigments_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        form = AssigmentF(request,
                          problems=[{"section":"Uno","amount":5},{"section":"Dos","amount":5},{"section":"Tres","amount":5},{"section":"Cuatro","amount":5}])
        assigments, course = await crud.get_assigments_course(course_id)
        assigments = sorted(assigments,reverse=True)

        response=templates.TemplateResponse(
            request=request,
            name="teacher/assigments.html",
            context= {
                "assigments":assigments,
                "form":form,
                "course_id":course_id,
                "course_id_":course.id,
                "current_user":current_user,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"}
        )
        return response
    return "401", "Not authorized"



@router.get("/{course_id}")
async def course_modify_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        students,course = await crud.get_students_from_course(course_id) 
        students = sorted(students, key=lambda s: s[0].firstname)
        response=templates.TemplateResponse(
            request=request,
            name="teacher/modify.html",
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

@router.get("/add_student/{course_id}")
async def add_student_teacher(course_id:str, request: Request, current_user: CurrentUser) -> HTMLResponse:
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.role is UserEnum.teacher:
        form = UserF(request)
        response=templates.TemplateResponse(
            request=request,
            name="teacher/add_student.html",
            context={
                "current_user":current_user,
                "form":form,
                "course_id":course_id,
                "elapsed_time_seconds":f"{elapsed_time():2.3f}"
            }
        )

        return response
    return "401", "Not authorized"



