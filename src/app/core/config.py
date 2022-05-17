from typing import Any, Optional
from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = "sqe_backend"
    SERVER_HOST: AnyHttpUrl = "http://localhost"
    PROJECT_NAME: str = "SQE-Welding-Project"
    # ToDo: store and access secrets properly
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:awesomepw@localhost:5432"
    DATABASE_URL_SYNC: str = "postgresql://postgres:awesomepw@localhost:5432"

settings = Settings()