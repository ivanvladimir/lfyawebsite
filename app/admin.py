from flask import Blueprint, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import *
from .model import UserEnum, User, UserRepository
from flask_login import LoginManager, login_user, logout_user, login_required, login_manager
import time
from .database import mongo

admin = Blueprint('admin', __name__)

users=UserRepository(database=mongo.db)

@admin.route("/")
def index():
    #  Time
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    return render_template("index.html",
        elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )

@admin.route("/login",methods=["GET","POST"])
def login():
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    form=AdminLogin()

    if form.validate_on_submit():
        user=users.find_one_by({'role':UserEnum.admin})
        if check_password_hash(user.password,form.password.data):
            login_user(user)
            return render_template("admin/home.html",
                elapsed_time_seconds= f'{elapsed_time():2.3f}'
                )
        else:
            return 404
    return render_template("admin/login.html",
            form=form,
            elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )

@admin.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

