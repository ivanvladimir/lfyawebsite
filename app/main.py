from flask import Blueprint, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import *
from .model import UserEnum, User, UserRepository
from flask_login import LoginManager, login_user, logout_user, login_required, login_manager
import time
from .database import mongo

main = Blueprint('main', __name__)

users=UserRepository(database=mongo.db)

@main.route("/")
def index():
    #  Time
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    return render_template("index.html",
        elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )

