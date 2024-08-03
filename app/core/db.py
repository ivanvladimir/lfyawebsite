import motor.motor_asyncio

from app.core.config import settings
client = motor.motor_asyncio.AsyncIOMotorClient(str(settings.MONGO_DATABASE_URI))
db  = client.LFYA

user_collection = db.users
course_teacher_collection = db.course_teacher
course_student_collection = db.course_student
course_collection = db.courses
