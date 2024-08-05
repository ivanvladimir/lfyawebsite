import uuid
import datetime
from typing import Any, List

from bson.objectid import ObjectId

from app.models import User, UserEnum, Course, Attendance
from app.core.db import user_collection, course_student_collection, course_teacher_collection, course_collection, attendance_unique_dates, attendance_collection

async def create_user(firstname: str, lastname:str, email:str, role: UserEnum)  -> User:
    dt = datetime.utcnow()
    user = User(
            role=role,
            email=email,
            lastname=lastname,
            firstname=firstname,
            url=str(uuid.uuid4()),
            created=dt,
            modified=dt,
        )
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

async def get_user(user_id:str) -> User | None:
    user = await user_collection.find_one(
        {"_id": ObjectId(user_id)}
    )
    if user:
        user['id']=user['_id']
        return User(**user)
    return user

def dict2course(g:dict ) -> Course:
    g['id']=g['_id']
    return Course(**g)

def dict2user(g:dict ) -> User:
    g['id']=g['_id']
    return User(**g)

def dict2attendance(g:dict ) -> Attendance:
    g['id']=g['_id']
    return Attendance(**g)

async def get_groups_teacher(user: User) -> List[Course]:
    groups_ids = course_teacher_collection.find({"teacher": str(user.id)})
    groups = [await course_collection.find_one(ObjectId(g['course'])) 
        for g in await groups_ids.to_list(100)]
    return [dict2course(g) for g in groups]

async def get_students_from_course(course_id: str) -> List[User]:
    course = await course_collection.find_one({"course_id": course_id})
    course = dict2course(course)
    student_ids = course_student_collection.find({"course": str(course.id)})
    course_student_info = {ObjectId(student_info['student']):student_info for student_info in await student_ids.to_list(100) }
    students = user_collection.find({"_id": {"$in": [k for k in course_student_info.keys()]}})
    return [ (dict2user(s),course_student_info[s["_id"]]['participation'],course_student_info[s["_id"]]['_id']) for s in await students.to_list(100)], course

async def get_students_from_course_date(course_id: str, date: str) -> List[User]:
    date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    course = await course_collection.find_one({"course_id": course_id})
    course = dict2course(course)
    student_ids = course_student_collection.find({"course": str(course.id)})
    course_student_info = {ObjectId(student_info['student']):student_info for student_info in await student_ids.to_list(100) }
    students = user_collection.find({"_id": {"$in": [k for k in course_student_info.keys()]}})
    students = {s['_id']:dict2user(s) for s in await students.to_list(100)}
    student_attendance = attendance_collection.find({"date": date })
    return [ (students[ObjectId(s_a['student'])],dict2attendance(s_a)) for s_a in await student_attendance.to_list(100)], course 

async def get_unique_dates_attendance_course(course_id: str) -> List[User]:
    course = await course_collection.find_one({"course_id": course_id})
    course = dict2course(course)
    dates = await attendance_unique_dates(str(course.id))
    return dates['values'], course

async def get_user_by_email(email: str) -> User | None:
    await user_collection.find_one({"email": email})
    return session_user

async def authenticate(secret_url:str) -> User | None:
    user = await user_collection.find_one({"url": secret_url})
    user['id']=user['_id']
    if user:
        return User(**user)
    else:
        return None

async def get_student(course_student_id: str) -> Any:
    return await course_student_collection.find_one({"_id": str(course_student_id)})

async def update_student(course_student_update) -> Any:
    return await course_student_collection.find_one({"_id": str(course_student_update)})

async def get_course_student(course_student_id: str) -> Any:
    res= await course_student_collection.find_one(
        {"_id": ObjectId(course_student_id)})
    return res

async def update_course_student(course_student_id,course_student_update) -> Any:
    return await course_student_collection.update_one(
        {"_id":ObjectId(course_student_id)},
        {"$set": course_student_update})
 
async def get_course_student_date(course_student_id: str, date: str) -> Any:
    res= await course_student_collection.find_one(
        {"_id": ObjectId(course_student_id)})
    return res

async def exists_date_course(course_id: str, date: datetime) -> Any:
    res= await course_student_collection.find_one(
        {"course": course_id,
         "date": date
         })
    if res:
        True
    else:
        False
    return res



