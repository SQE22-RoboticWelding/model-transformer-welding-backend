import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.api.deps import get_async_db
from app.db.base_class import Base
from app.main import app
from app.db.init_db import init_db_by_model


@pytest_asyncio.fixture(scope="function")
async def database(postgresql):
    connection_sync = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:" \
                      f"{postgresql.info.port}/{postgresql.info.dbname}"
    connection_async = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:' \
                       f'{postgresql.info.port}/{postgresql.info.dbname}'

    engine_sync = create_engine(connection_sync)
    engine_async = create_async_engine(connection_async)

    # Create database schema
    init_db_by_model(engine_sync)

    sessionmaker_async = sessionmaker(autocommit=False, autoflush=False, bind=engine_async, class_=AsyncSession)
    session_async = sessionmaker_async()
    try:
        yield session_async
    finally:
        await session_async.close()


@pytest.fixture(scope="function")
def database_engine_sync(postgresql):
    connection_sync = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:" \
                      f"{postgresql.info.port}/{postgresql.info.dbname}"
    engine_sync = create_engine(connection_sync)
    Base.metadata.create_all(bind=engine_sync)
    yield engine_sync


@pytest.fixture(scope="function")
def client(database): # noqa
    db = database
    client = AsyncClient(app=app, base_url="http://localhost")

    def override_get_db():
        yield db
    app.dependency_overrides[get_async_db] = override_get_db

    yield client
