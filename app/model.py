from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Union
from datetime import datetime, date, time
from pydantic_mongo import AbstractRepository, ObjectIdField


class UserEnum(str, Enum):
    admin = "admin"
    teacher = "teacher"
    teacher_assistant = "teacher_assistant"
    student = "student"


class AttendanceEnum(str, Enum):
    present = "present"
    justificated = "justificated"
    late = "late"
    absent = "absent"


class User(BaseModel):
    id: ObjectIdField = None
    role: UserEnum
    idunam: Optional[str]
    email: Optional[str]
    lastname: str
    firstname: str
    prefered_name: Optional[str]
    prefered_pronoun: Optional[str]
    url: Optional[str]
    password: Optional[str]
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


class UserRepository(AbstractRepository[User]):
    class Meta:
        collection_name = "users"


class Course(BaseModel):
    id: ObjectIdField = None
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

class CourseRepository(AbstractRepository[Course]):
    class Meta:
        collection_name = "courses"

class CourseTeacher(BaseModel):
    id: ObjectIdField = None
    teacher: str
    course: str
    notes: Optional[str]
    created: datetime
    modified: datetime


class CourseTeacherRepository(AbstractRepository[CourseTeacher]):
    class Meta:
        collection_name = "course_teacher"


class CourseStudent(BaseModel):
    id: ObjectIdField = None
    student: str
    course: str
    participation: int = 0
    grade: Optional[float]
    created: datetime
    modified: datetime


class CourseStudentRepository(AbstractRepository[CourseStudent]):
    class Meta:
        collection_name = "course_student"


class Attendance(BaseModel):
    id: ObjectIdField = None
    student: str
    course: str
    observations: Optional[str] = None
    date: datetime
    status: AttendanceEnum
    created: datetime
    modified: datetime


class AttendanceRepository(AbstractRepository[Attendance]):
    class Meta:
        collection_name = "attendance"
