from flask import Blueprint, render_template, redirect, url_for, current_app, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, login_manager, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import time
import yagmail
import markdown
from .forms import *
from .model import UserEnum, User, UserRepository
from .database import mongo

from flask_jwt_extended import create_access_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

admin = Blueprint('admin', __name__)

users=UserRepository(database=mongo.db)

@admin.route("/")
def index():
    #  Time
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    if current_user.is_authenticated:
        return render_template("admin/home.html",
            elapsed_time_seconds= f'{elapsed_time():2.3f}'
        )
    else:
        return redirect(url_for('admin.login'))


@admin.route("/login",methods=["GET","POST"])
def login():
    start_time = time.time()
    
    lapsed_time = lambda: time.time() - start_time

    form=AdminLogin()

    if form.validate_on_submit():
        user=users.find_one_by({'role':UserEnum.admin})
        if check_password_hash(user.password,form.password.data):
            login_user(user)
            access_token = create_access_token(identity=str(user.id))
            response= make_response(render_template("admin/home.html",
                elapsed_time_seconds= f'{elapsed_time():2.3f}'
                ))
            set_access_cookies(response, access_token)
            return response

        else:
            return 404
    return render_template("admin/login.html",
            form=form,
            elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )

@admin.route("/logout")
def logout():
    logout_user()
    response= make_response(redirect(url_for('admin.login')))
    unset_jwt_cookies(response)
    return response


@admin.route("/mail_to",methods=['GET','POST'])
@login_required
def mail_to():
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time

    form=MailTo()

    if form.validate_on_submit():
        yag= yagmail.SMTP(current_app.config.get('EMAIL_USER'))
        yag.send(form.to.data,
                form.subject.data,
                [markdown.markdown(form.msg.data)])
        return render_template("admin/mail_sent.html",
                form=form,
                elapsed_time_seconds= f'{elapsed_time():2.3f}'
                )

    return render_template("admin/mail_to.html",
            form=form,
            elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )


