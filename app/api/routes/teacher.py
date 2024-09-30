import time
import uuid
import datetime
import humanize
import random
from typing import Annotated, Any

from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import HTMLResponse

from app import crud
from app.api.deps import CurrentUser
from app.core import security
from app.core import uptime
from app.core.config import settings
from app.models import Token, UserEnum, Attendance, AttendanceEnum, User, Assigment

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
        msg = f"<strong>{int(course_student_['participation'])}</strong>"
        return HTMLResponse(content=msg,status_code=200)
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
        msg = f"<strong>{int(course_student_['participation'])}</strong>"
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")

@router.post("/attendance/create/{course_id}")
async def attendance_create_api_teacher(course_id: str, date: Annotated[str, Form()], request:Request, current_user: CurrentUser, response_class=HTMLResponse) -> HTMLResponse:
    """
    Create attendance for a class
    """
    if current_user.role is UserEnum.teacher:
        if await crud.exists_date_course(course_id=course_id,date=date):
            raise HTTPException(status_code=403, detail="Date already exists")
        students,course = await crud.get_students_from_course(str(course_id))
        
        atts =[]
        date_=datetime.datetime.strptime(date, "%d/%m/%Y")
        for s,_,_ in students:
            gt = datetime.datetime.utcnow()
            att = Attendance(
                student=str(s.id),
                course=str(course.id),
                date=date_,
                status=AttendanceEnum.present,
                created=gt,
                modified=gt,
            )
            atts.append(att)
        result = await crud.add_attendances(atts)
        msg= f"<li><a href='/class/teacher/{course_id}/attendance/modify/{date_}'><strong>{date}</strong></a></li>"
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")

@router.post("/assigment/create/{course_id}")
async def assigment_create_api_teacher(course_id: str, request:Request, current_user: CurrentUser, response_class=HTMLResponse) -> HTMLResponse:
    """
    Create assiment for a class
    """
    if current_user.role is UserEnum.teacher:
        assigment = dict(await request.form())
        if await crud.exists_assigment_course(course_id=course_id,assigment=assigment['name']):
            raise HTTPException(status_code=403, detail="Assigment already exists")
        students,course = await crud.get_students_from_course(str(course_id))
        
        assigments =[]
        for s,_,_ in students:
            gt = datetime.datetime.utcnow()
            assigments_=[]
            sections_=[]
            ini=0
            num=len([k for k in assigment.keys() if k.endswith("amount")])
            for problem in range(num):
                assigments_.append(ini+random.choices(list(range(int(assigment[f"problems-{problem}-amount"]))))[0])
                sections_.append(assigment[f"problems-{problem}-section"])
                ini+=int(assigment[f"problems-{problem}-amount"])
            att = Assigment(
                student=str(s.id),
                course=str(course.id),
                assigments=assigments_,
                name=assigment["name"],
                sections=sections_,
                created=gt,
                modified=gt,
            )
            assigments.append(att)
        result = await crud.add_assigments(assigments)
        #msg= f"<li><a href='/class/teacher/{course_id}/attendance/modify/{date_}'><strong>{date}</strong></a></li>"
        return HTMLResponse(content="<li>Hola</li>",status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")

@router.get("/status/{status}/{attendance_id}")
async def change_status_attendance_api_teacher(status: str, attendance_id: str, request:Request, current_user: CurrentUser, response_class=HTMLResponse) -> HTMLResponse:
    """Changin status assitance"""
    if current_user.role is UserEnum.teacher:
        att = await crud.get_attendance(attendance_id)
        if status == "present":
            att.status = AttendanceEnum.present
        if status == "justified":
            att.status = AttendanceEnum.justificated
        if status == "absent":
            att.status = AttendanceEnum.absent
        if status == "late":
            att.status = AttendanceEnum.late

        await crud.update_attendance(attendance_id=str(att.id), status=att.status, modified=datetime.datetime.utcnow())
        msg = f"<strong>{status}</strong>"
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")


@router.get("/switch/active/{student_id}")
async def switch_active_teacher(student_id: str, request:Request, current_user: CurrentUser) -> str:
    """
    Switch user from active to not active, or viceversa
    """
    if current_user.role is UserEnum.teacher:
        student = await crud.get_student(student_id)
        student_ = { 
            'active': False if student.active else True,
            'modified':datetime.datetime.utcnow()
        }
        await crud.update_student(student.id,student_)
        if student.active:
            msg = f"<span>❌</span>"
        else:
            msg = f"<span class='has-text-success'>✔</span>"
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")


@router.post("/add_student/{course_id}")
async def add_student_api_teacher(course_id: str, 
                                        idunam: Annotated[str, Form()], 
                                        firstname: Annotated[str, Form()], 
                                        lastname: Annotated[str, Form()], 
                                        email: Annotated[str, Form()], 
                                        request:Request, current_user: CurrentUser, response_class=HTMLResponse) -> HTMLResponse:
    """
    Create user
    """
    if current_user.role is UserEnum.teacher:
        gt = datetime.datetime.utcnow()
        s = User(
                role= UserEnum.student,
                idunam=idunam.strip(),
                firstname=firstname.upper().strip(),
                lastname=lastname.upper().strip(),
                email=email.strip(),
                created=gt,
                modified=gt,
                url=str(uuid.uuid4()),
                active=True,
            )
        result = await crud.create_student(s, course_id)
        
        msg= f""" <tr class="row">
            <td>
                { '<span class="has-text-success">✔</span>' if s.active else '<span>❌</span>'}
            </td>
            <td><a class="name" href="">{s.firstname} {s.lastname}</a></td>
            <td>{s.email}</td>
            <td>{s.idunam}</td>
            <td>{s.prefered_pronoun}</td>
            <td>{s.prefered_name}</td>
    </tr>"""
        return HTMLResponse(content=msg,status_code=200)
    else:
        raise HTTPException(status_code=401, detail="Not authorized")








