from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional, Union
from datetime import datetime
from pydantic_mongo import AbstractRepository, ObjectIdField

class UserEnum(str,Enum):
    admin = 'admin'
    teacher = 'teacher'
    teacher_assistant = "teacher_assistant"
    student = 'student'

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
    password: str = None
    created: datetime
    modified: datetime
    active: bool = True

    def to_json(self):
        return {"name":self.idunam,
                "url":self.url}

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
        collection_name = 'users'
