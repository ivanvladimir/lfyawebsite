from flask import Blueprint, current_app
import time

api = Blueprint('api', __name__)

__API_VERSION__="0.1.0"
__API_NAME__="API para Lenguajes Formales y Autómatas"


@api.route('/')
def info():
    """Prints info"""
    start_time = time.time()
    elapsed_time = lambda: time.time() - start_time
    return {
        'name': __API_NAME__,
        'version': __API_VERSION__,
        'status': current_app.config['STATUS'],
        "elapsed_time_seconds": f'{elapsed_time():2.3f}',
        'uptime': f"{time.time() - current_app.config['START_TIME']:2.3f} segs",
        }


