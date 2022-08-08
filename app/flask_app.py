from flask import Flask, request, render_template
import hmac
import hashlib
from functools import lru_cache
from html import escape
import git
import time
import subprocess


__VERSION__ = "0.1.0"
__APP_NAME__= "Lenguajes Formales y Autómatas"


def create_app(test_config=None):
    """Creates the App"""


    # Arrange configuration
    from . import config
    @lru_cache()
    def get_settings():
        return config.Settings()
    setting=get_settings()

    # create app
    app = Flask(__name__)
    app.config['START_TIME'] = time.time()
    app.config['STATUS'] = "Active"
    app.config['__APP_NAME__'] =  __APP_NAME__
    app.config['__VERSION__'] = __VERSION__


    # Import Blueprints
    from .api import api
    from .main import main
    app.register_blueprint(main)
    app.register_blueprint(api,url_prefix="/api")

    # Verifies token from webhook 
    def verify_signature(req):
        signature = "sha256="+hmac.new(
                bytes(setting.SECRET_TOKEN_WEBHOOK, 'utf-8'),
                msg = req.data,
                digestmod = hashlib.sha256
                ).hexdigest().lower()
        return hmac.compare_digest(signature, req.headers['X-Hub-Signature-256'])

    @app.route('/webhook', methods=['POST'])
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

