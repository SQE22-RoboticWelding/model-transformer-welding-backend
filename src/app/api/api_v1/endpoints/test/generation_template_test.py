import unittest
from typing import Any

import testing.postgresql
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.main import app
from app.api.deps import get_async_db
from app.db.base import Base
from app.models.generation_template import GenerationTemplate


class GenerationTemplateTest(unittest.TestCase):
    postgresql: testing.postgresql.Postgresql
    client: TestClient
    engine: Any
    engine_sync: Any
    session_sync: sessionmaker

    def setUp(self) -> None:
        self.postgresql = testing.postgresql.Postgresql(port=5678)
        self.engine_sync = create_engine("postgresql://postgres:awesomepw@localhost:5678", echo=True)
        self.engine = create_async_engine(
            "postgresql+asyncpg://postgres:xyz@localhost:5678",
            echo=True
        )
        self.session_sync = sessionmaker(autocommit=False, autoflush=False, bind=self.engine_sync)
        session_async = sessionmaker(autocommit=False, autoflush=False, bind=self.engine, class_=AsyncSession)

        Base.metadata.create_all(bind=self.engine_sync)
        self.engine_sync.execute(delete(GenerationTemplate))

        self.client = TestClient(app)

        def override_get_db():
            try:
                db = session_async()
                yield db
            finally:
                db.close()
        app.dependency_overrides[get_async_db] = override_get_db

    def tearDown(self) -> None:
        self.postgresql.stop()

    def test_get_empty(self):
        response = self.client.get("/api/v1/generationtemplate/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"[]", response.content)

    def test_get_all(self):
        with self.session_sync() as session:
            session.add(GenerationTemplate(id=1, name="My Template #1", content="X"))
            session.add(GenerationTemplate(id=2, name="My Template #2", content="Y"))
            session.commit()
        response = self.client.get("/api/v1/generationtemplate/")
        self.assertEqual(200, response.status_code)

        response_json = response.json()
        self.assertEqual(2, len(response_json))
        self.assertIn({**response_json[0], "id": 1, "name": "My Template #1", "content": "X"}, response_json)
        self.assertIn({**response_json[1], "id": 2, "name": "My Template #2", "content": "Y"}, response_json)

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
        with self.session_sync() as session:
            result = session.execute(select(GenerationTemplate)).scalars().all()
            self.assertEqual(1, len(result))
            self.assertEqual("My Template", result[0].name)
            self.assertEqual("Fill {{ this }}", result[0].content)
            self.assertEqual(None, result[0].description)

    def test_post_wrong_content_type(self):
        response = self.client.post("/api/v1/generationtemplate/",
                                    b'{"name": "My Template", "content": { "value": "{{fill}}" }}')
        self.assertEqual(400, response.status_code)

    def test_post_wrong_name_type(self):
        response = self.client.post("/api/v1/generationtemplate/",
                                    b'{"name": [5], "content": ""}')
        self.assertEqual(400, response.status_code)

    def test_post_missing_content(self):
        response = self.client.post("/api/v1/generationtemplate/",
                                    b'{"name": [5]}')
        self.assertEqual(400, response.status_code)

    def test_post_missing_name(self):
        response = self.client.post("/api/v1/generationtemplate/",
                                    b'{"content": ""}')
        self.assertEqual(400, response.status_code)
