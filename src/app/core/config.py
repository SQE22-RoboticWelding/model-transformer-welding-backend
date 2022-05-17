from typing import Any, Optional
from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "sqe_backend"
    SERVER_HOST: AnyHttpUrl =  "http://localhost"
    PROJECT_NAME: str = "SQE-Welding-Project"
    # ToDo: store and access secrets properly
    DATABASE_URL: str = "postgresql+asyncpg://postgres:awesomepw@sqe_database:5432"

settings = Settings()