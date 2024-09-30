import motor.motor_asyncio
from bson import SON

from app.core.config import settings
client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.MONGO_DATABASE_URI))
db  = client.LFYA

user_collection = db.users
course_teacher_collection = db.course_teacher
course_student_collection = db.course_student
course_collection = db.courses
attendance_collection = db.attendance
assigment_collection = db.assigment

async def attendance_unique_dates(course_id:str):
    response= await db.command(SON(
        [
            ("distinct","attendance"),
            ("key","date"),
            ("query",{"course":course_id})
        ],
    ))
    return response

async def assigments_course(course_id:str):
    response= await db.command(SON(
        [
            ("distinct","assigment"),
            ("key","name"),
            ("query",{"course":course_id})
        ],
    ))
    return response

   
