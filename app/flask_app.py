from flask import Flask, request
from functools import lru_cache
from html import escape
import git
import time

def create_app(test_config=None):
    # Arrange configuration
    from . import config
    @lru_cache()
    def get_settings():
        return config.Settings()
    setting=get_settings()

    # create app
    app = Flask(__name__)

    @app.route('/webhook', methods=['POST'])
    def webhook():
        if request.method == 'POST':
            info=request.get_json()
            repo = git.Repo("./lfyawebsite")
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated successfull', 200
        else:
            return '', 400

    # Call by arguments: api/?max_length=200&num_beams=2&top_p=0.95&seed=1337
    @app.route("/")
    def main():
        #  Time
        start_time = time.time()
        elapsed_time = lambda: time.time() - start_time
        res={
            "elapsed_time_seconds": f'{elapsed_time():2.3f}',
        }
        return res

    return app

app=create_app()

