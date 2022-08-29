from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import *
from .model import UserEnum, User, UserRepository
from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    login_manager,
)
import time
from .database import mongo

student = Blueprint("student", __name__)

users = UserRepository(database=mongo.db)


@admin.route("/{url}", methods=["GET"])
def login(url):
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    user = users.find_one_by({"url": url})
    if user:
        login_user(user)
        return render_template(
            "students/home.html", elapsed_time_seconds=f"{elapsed_time():2.3f}"
        )
    else:
        return 404, "URL invalid"


@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("admin.login"))
