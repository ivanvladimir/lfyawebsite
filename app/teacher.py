from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    current_app,
    make_response,
)
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    login_manager,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import *
from .model import *
import time
import random
import humanize
from .database import mongo
from bson.objectid import ObjectId

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

teacher = Blueprint("teacher", __name__)

users = UserRepository(database=mongo.db)
courses = CourseRepository(database=mongo.db)
attendance = AttendanceRepository(database=mongo.db)
course_student = CourseStudentRepository(database=mongo.db)
course_teacher = CourseTeacherRepository(database=mongo.db)


@teacher.route("/", methods=["GET"])
def index():
    #  Time
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.is_authenticated:
        groups_ids = course_teacher.find_by({"teacher": str(current_user.id)})
        groups = [courses.find_one_by_id(ObjectId(g.course)) for g in groups_ids]
        return render_template(
            "teacher/home.html",
            groups=groups,
            elapsed_time_seconds=f"{elapsed_time():2.3f}",
        )
    else:
        return redirect(url_for("admin.login"))


@teacher.route("/<url>", methods=["GET"])
def login(url):
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    user = users.find_one_by({"url": url})
    if user:
        login_user(user)
        access_token = create_access_token(identity=str(user.id))
        response = make_response(
            render_template(
                "teacher/home.html", elapsed_time_seconds=f"{elapsed_time():2.3f}"
            )
        )
        set_access_cookies(response, access_token)
        return response
    else:
        return 404, "URL invalid"


@teacher.route("/logout")
def logout():
    logout_user()
    response = make_response(redirect(url_for("main.index")))
    unset_jwt_cookies(response)
    return response


@teacher.route("/<course_id>/list", methods=["GET"])
@login_required
def list(course_id):
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if not current_user.role == UserEnum.teacher:
        return "401", "Not authorized"

    course = courses.find_one_by({"course_id": course_id})
    student_ids = course_student.find_by({"course": str(course.id)})
    students = [
        (users.find_one_by_id(ObjectId(s.student)), s.participation, str(s.id))
        for s in student_ids
    ]

    students = sorted(students, key=lambda s: s[0].firstname)
    return render_template(
        "teacher/list.html",
        students=students,
        course_id=course_id,
        elapsed_time_seconds=f"{elapsed_time():2.3f}",
    )


@teacher.route("/<course_id>/attendance/list", methods=["GET"])
@login_required
def attendance_list(course_id):
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if not current_user.role == UserEnum.teacher:
        return "401", "Not authorized"

    form = DateF()
    course = courses.find_one_by({"course_id": course_id})
    days = attendance.find_by({"course": str(course.id)})
    days = set(d.date for d in days)
    days = [(d,humanize.naturaldate(d)) for d in sorted(days,reverse=True)]

    return render_template(
        "teacher/attendance_list.html",
        days=days,
        form=form,
        course_id=course_id,
        elapsed_time_seconds=f"{elapsed_time():2.3f}",
    )


@teacher.route("/<course_id>/attendance/modify/<date>", methods=["GET"])
@login_required
def attendance_date(course_id, date):
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if not current_user.role == UserEnum.teacher:
        return "401", "Not authorized"

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

    return render_template(
        "teacher/attendance.html",
        course_id_=str(course.id),
        course_id=course_id,
        date=date,
        students=students,
        elapsed_time_seconds=f"{elapsed_time():2.3f}",
    )
