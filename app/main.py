from flask import Blueprint, render_template
import time

main = Blueprint('main', __name__)

@main.route("/")
def index():
    #  Time
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    return render_template("index.html",
        elapsed_time_seconds= f'{elapsed_time():2.3f}'
    )

