from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import core_schema
from enum import Enum
from bson import ObjectId
from typing import List, Optional, Union, Any, Annotated
from datetime import datetime, date, time
from pydantic_mongo import AbstractRepository, PydanticObjectId

class UserEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    teacher_assistant = "teacher_assistant"
    student = "student"

class AttendanceEnum(str, Enum):
    present = "present"
    justificated = "justificated"
    justific = "justificated"
    late = "late"
    absent = "absent"

class User(BaseModel):
    id: Optional[PydanticObjectId] = None
    role: UserEnum
    idunam: Optional[str] = None
    email: Optional[str] = None
    lastname: str
    firstname: str
    prefered_name: Optional[str] = None
    prefered_pronoun: Optional[str] = None
    url: Optional[str] = None
    password: Optional[str] = None
    created: datetime
    modified: datetime
    active: bool = True

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Course(BaseModel):
    id: Optional[PydanticObjectId] = None
    course_name: str = "Lenguajes Formales y Automatas"
    institution: str = "Faculad de Ingeniería, Universidad Nacional Autónoma de México"
    initials: str = "LFYA"
    course_id: str
    year: str
    semester: str
    created: datetime
    modified: datetime
    info: Optional[str]
    links: Optional[dict]
    starting_date: Optional[date]
    finishes_date: Optional[date]
    starting_time: Optional[time]
    finishin_time: Optional[time]
    active: bool = True

class CourseTeacher(BaseModel):
    id: Optional[PydanticObjectId] = None
    teacher: str
    course: str
    notes: Optional[str]
    created: datetime
    modified: datetime


class CourseStudent(BaseModel):
    id: Optional[PydanticObjectId] = None
    student: str
    course: str
    participation: int = 0
    grade: Optional[float]
    created: datetime
    modified: datetime

class Attendance(BaseModel):
    id: Optional[PydanticObjectId] = None
    student: str
    course: str
    observations: Optional[str] = None
    date: datetime
    status: AttendanceEnum
    created: datetime
    modified: datetime

# Contents of JWT token
class TokenPayload(BaseModel):
    subject: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
