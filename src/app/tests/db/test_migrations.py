import sqlalchemydiff
from pytest_postgresql import factories
import tempfile
from sqlalchemy import create_engine
from app.db.init_db import init_db_by_model
from app.core.config import settings

socket_dir = tempfile.TemporaryDirectory()

# Get another database by using another fixture
postgresql_my_proc = factories.postgresql_proc(port=None, unixsocketdir=socket_dir.name)
postgresql_db_2 = factories.postgresql("postgresql_my_proc")


def test_migrations(database_engine_sync, postgresql_db_2):
    def get_db_engine_by_model():
        connection_url_sync = f"postgresql+psycopg2://{postgresql_db_2.info.user}:@{postgresql_db_2.info.host}:" \
                          f"{postgresql_db_2.info.port}/{postgresql_db_2.info.dbname}"
        engine_sync = create_engine(connection_url_sync)

        # Run db schema creation by model
        init_db_by_model(engine_sync)
        return engine_sync

    database_engine_sync_model = get_db_engine_by_model()

    # Compares both databases, whether tables and columns are identical. Ignore 'alembic_version' as this is the table
    # for keeping tracks of migrations
    result = sqlalchemydiff.comparer.compare(
        database_engine_sync.url,
        database_engine_sync_model.url,
        ignores=["alembic_version"]
    )
    
    # Cleanup directory of second db
    socket_dir.cleanup()

    # Only printed on error
    print(result.errors)
    assert result.is_match
