from typing import AsyncGenerator, Generator
from app.db.session import async_session_local, sync_session_local


def get_sync_db() -> Generator:
    try:
        db = sync_session_local()
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncGenerator:
    async with async_session_local() as session:
        yield session
