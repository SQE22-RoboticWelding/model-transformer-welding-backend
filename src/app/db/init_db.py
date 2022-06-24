from app.db.base import Base
from getter import get_path
from alembic.config import Config
from alembic import command


def init_db_by_migrations(database_url_sync: str):
    alembic_config = Config()
    alembic_config.set_main_option("script_location", f"{get_path()}/alembic")
    alembic_config.set_main_option("sqlalchemy.url", database_url_sync)
    command.upgrade(alembic_config, 'head')


def init_db_by_model(engine_sync):
    Base.metadata.create_all(bind=engine_sync)
