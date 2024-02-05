from flask import Blueprint, current_app, request, url_for
from flask_jwt_extended import jwt_required
import random
import humanize
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
    course = courses.find_one_by_id(ObjectId(course_id))
    students = course_student.find_by({"course": course_id})

    date = request.form["date"]
    atts =[]
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
        atts.append(att)
    attendance.save_many(atts)

    days = attendance.find_by({"course": course_id})
    days = list(set(d.date.date() for d in days))
    days = sorted(days,reverse=True)

    days = [f'<li><a href="{url_for("teacher.attendance_date",course_id=course.course_id, date=datetime.strftime(date, "%Y-%m-%d %H:%M:%S"))}">{humanize.naturaldate(d)}</a></li>' 
            for d in days]

    return "\n".join(days)


@api.route("/<course_id>/attendance/list/<date>", methods=["GET"])
@jwt_required()
def attendance_list(course_id,date):
    """Changin points"""
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    course = courses.find_one_by({"course_id": course_id})
    student_ids = course_student.find_by({"course": str(course.id)})
    attendance_student=attendance.find_by({"date": date})
    students_ = {
            s.student:users.find_one_by_id(ObjectId(s.student))
        for s in student_ids
    }
    students = [(students_[a_s.student],a_s)
            for a_s in attendance_student
            ]

    students = sorted(students, key=lambda s: s[0].firstname)
    if 'random' in request.args:
        random.shuffle(students)

    bits=[]
    for index,(s,a) in enumerate(students):
        s=f"""<tr class="row">
        <td><a class="name"  href="">{s.firstname} {s.lastname}</a></td>
        <td><a class="button is-success {'is-light' if not a.status=='present' else '' }"
           hx-get="{url_for('api.change_status_attendance',status='present',attendance_id=a.id)}" hx-target='#status-{index}'
            >Presente</a> </td>
        <td><a class="button is-danger {'is-light' if not a.status=='absent' else '' }"
           hx-get="{url_for('api.change_status_attendance',status='absent',attendance_id=a.id)}" hx-target='#status-{index}'
            >Ausente</a> </td>
        <td><a class="button is-warning {'is-light' if not a.status=='late' else '' }"
           hx-get="{url_for('api.change_status_attendance',status='late',attendance_id=a.id)}" hx-target='#status-{index}'
            >Retardo</a> </td>
        <td><a class="button is-info {'is-light' if not a.status=='justified' else '' }"
           hx-get="{url_for('api.change_status_attendance',status='justified',attendance_id=a.id)}" hx-target='#status-{index}'
            >Jusitificado</a> </td>
        <td id="status-{index}">{a.status}</td>
        <tr>"""
        bits.append(s)
    return "\n".join(bits)

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
