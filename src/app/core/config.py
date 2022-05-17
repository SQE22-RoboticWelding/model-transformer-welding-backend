import os
from pydantic import AnyHttpUrl, BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str = os.getenv("SERVER_NAME", "sqe_backend")
    SERVER_HOST: AnyHttpUrl = os.getenv("SERVER_HOST", "http://localhost")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "SQE-Welding-Project")
    # ToDo: store and access secrets properly
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC", f"postgresql+asyncpg://postgres:awesomepw@localhost:5432")
    DATABASE_URL_SYNC: str = os.getenv("DATABASE_URL_SYNC", "postgresql://postgres:awesomepw@localhost:5432")

settings = Settings()