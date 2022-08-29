from flask import Blueprint, current_app, request
from flask_jwt_extended import jwt_required
from .model import *
from .database import mongo
from datetime import datetime

from bson.objectid import ObjectId

import time

api = Blueprint("api", __name__)

users = UserRepository(database=mongo.db)
courses = CourseRepository(database=mongo.db)
attendance = AttendanceRepository(database=mongo.db)
course_student = CourseStudentRepository(database=mongo.db)
course_teacher = CourseTeacherRepository(database=mongo.db)

__API_VERSION__ = "0.1.0"
__API_NAME__ = "API para Lenguajes Formales y Autómatas"


@api.route("/")
def info():
    """Prints info"""
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    return {
        "name": __API_NAME__,
        "version": __API_VERSION__,
        "status": current_app.config["STATUS"],
        "elapsed_time_seconds": f"{elapsed_time():2.3f}",
        "uptime": f"{time.time() - current_app.config['START_TIME']:2.3f} segs",
    }


@api.route("/test")
@jwt_required()
def test():
    """Testing access"""
    return "<ul><li>One</li><li>Two</li><li>Three</li></ul>"


@api.route("/add/<course_student_id>")
def add(course_student_id):
    """Changin points"""
    student = course_student.find_one_by_id(ObjectId(course_student_id))
    student.participation += 1
    student.modified = datetime.utcnow()
    course_student.save(student)
    return f"<strong>{student.participation}</strong>"


@api.route("/substract/<course_student_id>")
@jwt_required()
def substract(course_student_id):
    """Changin points"""
    student = course_student.find_one_by_id(ObjectId(course_student_id))
    student.participation -= 1
    student.modified = datetime.utcnow()
    course_student.save(student)
    return f"<strong>{student.participation}</strong>"


@api.route("/create_attendance/<course_id>", methods=["POST"])
@jwt_required()
def create_attendance(course_id):
    """Changin points"""
    students = course_student.find_by({"course": course_id})

    date = request.form["date"]
    for s in students:
        gt = datetime.utcnow()
        att = Attendance(
            student=s.student,
            course=course_id,
            date=datetime.strptime(date, "%d/%m/%Y"),
            status=AttendanceEnum.present,
            created=gt,
            modified=gt,
        )
        attendance.save(att)

    days = attendance.find_by({"course": course_id})
    days = set(d.date.date() for d in days)

    days = [f"<li>{d}</li>" for d in sorted(days)]

    return "\n".join(days)


@api.route("/status/<status>/<attendance_id>")
@jwt_required()
def change_status_attendance(status, attendance_id):
    """Changin points"""
    att = attendance.find_one_by_id(ObjectId(attendance_id))
    if status == "present":
        att.status = AttendanceEnum.present
    if status == "justified":
        att.status = AttendanceEnum.justificated
    if status == "absent":
        att.status = AttendanceEnum.absent
    if status == "late":
        att.status = AttendanceEnum.late

    att.modified = datetime.utcnow()
    attendance.save(att)
    return f"<strong>{att.status}</strong>"
