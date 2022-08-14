import click
from flask import Flask, request, render_template
from flask.cli import AppGroup
from flask_login import LoginManager
from logging.config import dictConfig
import hmac
import yagmail
import hashlib
import getpass
from functools import lru_cache
from html import escape
import git
import time
import subprocess
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
from .model import UserEnum, User, UserRepository, Course, CourseRepository
from .utils import read_value, chose_value

__VERSION__ = "0.1.0"
__APP_NAME__= "Lenguajes Formales y Autómatas"


def create_app(test_config=None):
    """Creates the App"""

    # Arrange configuration
    from . import config
    from .database import mongo
    @lru_cache()
    def get_settings():
        return config.Settings()

    setting=get_settings()
    # Configuring logging
    dictConfig(setting.LOGGING_CONFIG)

    # Configuring authentification
    login_manager = LoginManager()

    # create app
    app = Flask(__name__)
    user_cli = AppGroup('user')
    admin_cli = AppGroup('admin')
    course_cli = AppGroup('course')

	# Initialazing variables
    app.config['START_TIME'] = time.time()
    app.config['STATUS'] = "Active"
    app.config['__APP_NAME__'] =  __APP_NAME__
    app.config['__VERSION__'] = __VERSION__
    app.config['SECRET_KEY'] = setting.SECRET_KEY
    app.config['WTF_CSRF_SECRET_KEY'] = setting.WTF_CSRF_SECRET_KEY
    app.config['MONGO_URI'] = setting.DATABASE_MONGO_URI
    app.config['EMAIL_USER'] = setting.EMAIL_USER
     
    # Initaalazing modules
    login_manager.init_app(app)
    mongo.init_app(app)
    app.logger.info("Connected to DB")

    # Import Blueprints
    from .api import api
    from .main import main
    from .admin import admin
    app.register_blueprint(main,
            static_url_path='/static',
            static_folder='static')
    app.register_blueprint(admin,
            static_url_path='/static',
            static_folder='static', url_prefix="/admin")
    app.register_blueprint(api,url_prefix="/api")

    users=UserRepository(database=mongo.db)

    # Connecting to database
    @login_manager.user_loader
    def load_user(user_id):
        return users.find_one_by_id(ObjectId(user_id))


    login_manager.blueprint_login_views = {
            'main': '/admin/login',
            }

    # Flask commands
    @admin_cli.command('register_email')
    def register_email():

        passwd=getpass.getpass(f"Introduce password para {setting.EMAIL_USER}")
        yagmail.register(setting.EMAIL_USER, passwd) 

    @user_cli.command('initdb')
    def init_db():
        collection_names=set(mongo.db.collection_names())
        collection_names_to_create=set(['users','forum','activities','activity'])
        if len(collection_names.intersection(collection_names_to_create))>0:
            print(f"Error: Database with collections: {collection_names.intersection(collection_names_to_create)} ")
            return

        users=UserRepository(database=mongo.db)

        email= read_value("Correo electrónico:")
        firstname= read_value("Nombre (sin apellidos):")
        lastname= read_value("Apellidos:")
        password = generate_password_hash(read_value("Password:",passwd=True))
        dt = datetime.utcnow()

        student = User(
            role= UserEnum.student,
            email=email,
            lastname=lastname,
            firstname=firstname,
            password=password,
            created=dt,
            modified=dt)
        users.save(student)

    @user_cli.command('add')
    def create_user():
        users=UserRepository(database=mongo.db)

        email= read_value("Correo electrónico:")
        firstname= read_value("Nombre (sin apellidos):")
        lastname= read_value("Apellidos:")
        role = chose_value("Role:",{"estudiante":UserEnum.student, 'teacher':UserEnum.teacher, "ayudante":UserEnum.teacher_assistant})
        dt = datetime.utcnow()

        user = User(
            role= role,
            email=email,
            lastname=lastname,
            firstname=firstname,
            url=str(uuid.uuid4()),
            created=dt,
            modified=dt)
        users.save(user)

    @course_cli.command('add')
    def create_course():
        courses=CourseRepository(database=mongo.db)

        name= read_value("Nombre:")
        initials= read_value("Iniciales:")
        year= read_value("Año (eg. 2023):")
        semester = read_value("Semestre (1 o 2):")
        dt = datetime.utcnow()

        course = Course(
                name=name,
                initials=initials,
                year=year,
                semester=semester,
                course_id=f"{initials.lower()}{year[-2:]}{'i' if semester=='1' else 'ii'}",
                created=dt,
                modified=dt)
        courses.save(course)

    # Adding commands
    app.cli.add_command(user_cli)
    app.cli.add_command(course_cli)
    app.cli.add_command(admin_cli)

    # Verifies token from webhook 
    def verify_signature(req):
        signature = "sha256="+hmac.new(
                bytes(setting.SECRET_TOKEN_WEBHOOK, 'utf-8'),
                msg = req.data,
                digestmod = hashlib.sha256
                ).hexdigest().lower()
        return hmac.compare_digest(signature, req.headers['X-Hub-Signature-256'])

    @app.route('/webhook', methods=['POST'])
    # Webhook to reload code from pythonanywhere
    def webhook():
        if request.method == 'POST':
            if verify_signature(request):
                repo = git.Repo("./lfyawebsite")
                origin = repo.remotes.origin
                origin.pull()
                return 'Updated successfull', 200
            else:
                return 'Forbidden', 403
        else:
            return 'Not allowed', 405

    return app

app=create_app()

