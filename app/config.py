from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "LYA Website"
    SECRET_TOKEN_WEBHOOK: str = ""
    SECRET_KEY: str = "un secreto aquí"
    WTF_CSRF_SECRET_KEY: str = "otro secreto acá"
    DATABASE_MONGO_URI: str=""
    LOGGING_CONFIG: dict={
        'version': 1,
        'formatters': {'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                    }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
                    }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
            }
        }

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

