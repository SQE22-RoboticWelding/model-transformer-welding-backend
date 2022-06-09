import unittest
from typing import Any

import testing.postgresql
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from app.main import app
from app.api.deps import get_async_db
from app.db.base import Base
from app.models.generation_template import GenerationTemplate
from app.models.welding_configuration import WeldingConfiguration
from app.models.welding_point import WeldingPoint


class GenerationTemplateTest(unittest.TestCase):
    postgresql: testing.postgresql.Postgresql
    client: TestClient
    engine: Any
    engine_sync: Any
    template = ("{% for p in welding_points %}"
                "{{p.x}}, {{p.y}}, {{p.z}} / {{p.roll}}, {{p.pitch}}, {{p.yaw}} / {{p.welding_order}}"
                "{% endfor %}")
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

        self.engine_sync.execute(delete(WeldingPoint))
        self.engine_sync.execute(delete(WeldingConfiguration))
        self.engine_sync.execute(delete(GenerationTemplate))
        Base.metadata.create_all(bind=self.engine_sync)

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

    def test_post(self):
        with self.session_sync() as session:
            session.add(GenerationTemplate(id=1, name="My Template", content=self.template))
            session.add(WeldingConfiguration(id=1, name="My WeldingConfig"))
            session.add(WeldingPoint(welding_configuration_id=1,
                                     welding_order=0,
                                     x=10, y=5.5, z=0.25, roll=0.35, pitch=3, yaw=0))
            session.commit()
        response = self.client.post("/api/v1/codegeneration/generate",
                                    b'{"generation_template_id": 1, "welding_configuration_id": 1}')
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'"10.0, 5.5, 0.25 / 0.35, 3.0, 0.0 / 0"', response.content)
