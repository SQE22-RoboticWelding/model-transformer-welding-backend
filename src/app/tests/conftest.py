import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.api.deps import get_async_db
from app.db.base_class import Base
from app.main import app
from app.db.init_db import init_db_by_migrations


@pytest_asyncio.fixture(scope="function")
async def database_async_sessionmaker(postgresql):
    connection_sync = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:" \
                      f"{postgresql.info.port}/{postgresql.info.dbname}"
    connection_async = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:' \
                       f'{postgresql.info.port}/{postgresql.info.dbname}'

    engine_async = create_async_engine(connection_async)

    # Create database schema
    init_db_by_migrations(connection_sync)

    sessionmaker_async = sessionmaker(autocommit=False, autoflush=False, bind=engine_async, class_=AsyncSession)
    yield sessionmaker_async


@pytest.fixture(scope="function")
def database_engine_sync(postgresql):
    connection_sync = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:" \
                      f"{postgresql.info.port}/{postgresql.info.dbname}"
    engine_sync = create_engine(connection_sync)
    init_db_by_migrations(connection_sync)
    yield engine_sync


@pytest_asyncio.fixture(scope="function")
async def database(database_async_sessionmaker):
    session_async = database_async_sessionmaker()
    try:
        yield session_async
    finally:
        await session_async.close()


@pytest.fixture(scope="function")
def client(database_async_sessionmaker): # noqa
    db = database
    client = AsyncClient(app=app, base_url="http://localhost")

    async def override_get_db():
        session_async = database_async_sessionmaker()
        try:
            yield session_async
        finally:
            await session_async.close()
    app.dependency_overrides[get_async_db] = override_get_db

    yield client
