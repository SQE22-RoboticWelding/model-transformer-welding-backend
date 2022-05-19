from app.db.base import Base
from app.db.session import engine_sync


def init_db():
    Base.metadata.create_all(bind=engine_sync)
