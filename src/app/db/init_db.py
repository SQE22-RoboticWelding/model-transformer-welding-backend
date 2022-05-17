from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.db.base import Base
from app.db.session import engine_sync


def init_db():
    Base.metadata.create_all(bind=engine_sync)
