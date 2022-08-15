from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "LYA Website"
    SECRET_TOKEN_WEBHOOK: str = ""
    SECRET_KEY: str = "un secreto aquí"
    WTF_CSRF_SECRET_KEY: str = "otro secreto acá"
    DATABASE_MONGO_URI: str=""
    EMAIL_USER: str=""
    JWT_COOKIE_SECURE: bool = True
    JWT_SECRET_KEY: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

