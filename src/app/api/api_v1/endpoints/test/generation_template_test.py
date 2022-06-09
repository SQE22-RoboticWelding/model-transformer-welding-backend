import unittest
from typing import Any

import testing.postgresql
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.main import app
from app.api.deps import get_async_db
from app.db.base import Base


class GenerationTemplateTest(unittest.TestCase):
    postgresql: testing.postgresql.Postgresql
    client: TestClient
    engine: Any
    engine_sync: Any

    @classmethod
    def setUpClass(cls) -> None:
        cls.postgresql = testing.postgresql.Postgresql(port=5678)
        cls.engine_sync = create_engine("postgresql://postgres:awesomepw@localhost:5678", pool_pre_ping=True)
        cls.engine = create_async_engine(
            "postgresql+asyncpg://postgres:xyz@localhost:5678",
            echo=True
        )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine, class_=AsyncSession)

        def override_get_db():
            try:
                db = TestingSessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_async_db] = override_get_db
        cls.client = TestClient(app)
        Base.metadata.create_all(bind=cls.engine_sync)

    @classmethod
    async def tearDownClass(cls) -> None:
        await Base.metadata.drop_all(bind=cls.engine_sync)
        cls.postgresql.stop()

    def test_get(self):
        response = self.client.get("/api/v1/generationtemplate/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"[]")

    def test_post(self):
        response = self.client.post("/api/v1/generationtemplate/",
                                    b'{"name": "My Template", "content": "Fill {{ this }}"}')
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(
            response.json(),
            {
                **response.json(), "name": "My Template",
                "description": None,
                "content": "Fill {{ this }}"
            }
        )
