import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.api.deps import get_async_db
from app.db.base_class import Base
from app.main import app


@pytest_asyncio.fixture(scope="function")
async def database(postgresql):
    connection_sync = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:" \
                      f"{postgresql.info.port}/{postgresql.info.dbname}"
    connection_async = f'postgresql+asyncpg://{postgresql.info.user}:@{postgresql.info.host}:' \
                       f'{postgresql.info.port}/{postgresql.info.dbname}'

    engine_sync = create_engine(connection_sync)
    engine_async = create_async_engine(connection_async)

    # Create database schema
    Base.metadata.create_all(bind=engine_sync)

    sessionmaker_async = sessionmaker(autocommit=False, autoflush=False, bind=engine_async, class_=AsyncSession)
    session_async = sessionmaker_async()
    try:
        yield session_async
    finally:
        await session_async.close()


@pytest.fixture(scope="function")
def client(database):
    db = database
    client = AsyncClient(app=app, base_url="http://localhost")

    def override_get_db():
        yield db
    app.dependency_overrides[get_async_db] = override_get_db

    yield client
