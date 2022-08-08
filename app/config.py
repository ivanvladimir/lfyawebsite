from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "LFYA Website"
    SECRET_TOKEN_WEBHOOK: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

