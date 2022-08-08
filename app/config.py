from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    app_name: str = "LFYA Website"

    class Config:
        env_file = ".env"

