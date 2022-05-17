from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


engine_sync = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)
sync_session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine_sync)

engine_async = create_async_engine(settings.DATABASE_URL_ASYNC, pool_pre_ping=True)
async_session_local = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=engine_async)
