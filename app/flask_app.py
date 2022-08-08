from flask import Flask, request, render_template
from hmac import HMAC, compare_digest
from hashlib import sha256
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

    setting.SECRET_TOKEN_WEBHOOK.encode()

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
        received_sign = req.headers.get('X-Hub-Signature-256').split('sha256=')[-1].strip()
        secret = setting.SECRET_TOKEN_WEBHOOK.encode()
        expected_sign = HMAC(key=secret, msg=req.data, digestmod=sha256).hexdigest()
        return compare_digest(received_sign, expected_sign)

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

