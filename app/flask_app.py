import click
from flask import Flask, request, render_template
from flask.cli import AppGroup
from flask_login import LoginManager
from logging.config import dictConfig
import hmac
import hashlib
from functools import lru_cache
from html import escape
import git
import time
import subprocess
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


__VERSION__ = "0.1.0"
__APP_NAME__= "Lenguajes Formales y Autómatas"


def create_app(test_config=None):
    """Creates the App"""

    # Arrange configuration
    from . import config
    from . import database
    @lru_cache()
    def get_settings():
        return config.Settings()

    @lru_cache()
    def get_database():
        return database.get_mongo()

    setting=get_settings()
    mongo=get_database()
    # Configuring logging
    dictConfig(setting.LOGGING_CONFIG)

    # Configuring authentification
    login_manager = LoginManager()

    # create app
    app = Flask(__name__)
    user_cli = AppGroup('user')

	# Initialazing variables
    app.config['START_TIME'] = time.time()
    app.config['STATUS'] = "Active"
    app.config['__APP_NAME__'] =  __APP_NAME__
    app.config['__VERSION__'] = __VERSION__
    app.config['SECRET_KEY'] = setting.SECRET_KEY
    app.config['WTF_CSRF_SECRET_KEY'] = setting.WTF_CSRF_SECRET_KEY
    app.config["MONGO_URI"] = setting.DATABASE_MONGO_URI

    # Initaalazing modules
    login_manager.init_app(app)
    mongo.init_app(app)
    app.logger.info("Connected to DB")

    # Import Blueprints
    from .api import api
    from .main import main
    app.register_blueprint(main,
            static_url_path='/static',
            static_folder='static')
    app.register_blueprint(api,url_prefix="/api")

    # Connecting to database

    # Flask commands
    @user_cli.command('initdb')
    def create_user():
        import getpass
        from .model import UserEnum, User, UserRepository

        def read_value(info, passwd=False):
            value=input(info) if not passwd else getpass.getpass(info)
            while len(value.strip())==0:
                print("Sin valor, intentar de nuevo")
                value=input(info) if not passwd else getpass.getpass(info)
            return value

        collection_names=set(mongo.db.collection_names())
        collection_names_to_create=set(['users','forum','activities','activity'])
        if len(collection_names.intersection(collection_names_to_create))>0:
            print(f"Error: Database with collections: {collection_names.intersection(collection_names_to_create)} ")
            return

        users=UserRepository(database=mongo.db)

        for collection_name in collection_names_to_create:
            mongo.db[collection_name]
            app.logger.info(f"Colletion created {collection_name}")

        email= read_value("Correo electrónico:")
        firstname= read_value("Nombre (sin apellidos):")
        lastname= read_value("Apellidos:")
        password = generate_password_hash(read_value("Password:",passwd=True))
        dt = datetime.utcnow()

        admin = User(
            role= UserEnum.admin,
            email=email,
            lastname=lastname,
            firstname=firstname,
            password=password,
            created=dt,
            modified=dt)
        users.save(admin)

    # Adding commands
    app.cli.add_command(user_cli)

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

