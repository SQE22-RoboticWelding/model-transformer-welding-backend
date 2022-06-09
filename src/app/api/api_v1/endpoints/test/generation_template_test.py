import contextlib
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_sync_db
from app.db.base import Base


engine = create_engine(
    "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}, echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_sync_db] = override_get_db
client = TestClient(app)


class GenerationTemplateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Base.metadata.create_all(bind=engine)

    def setUp(self) -> None:
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        # meta = MetaData()
        # with contextlib.closing(engine.connect()) as con:
        #     trans = con.begin()
        #     for table in reversed(meta.sorted_tables):
        #         con.execute(table.delete())
        #     trans.commit()

    @classmethod
    def tearDownClass(cls) -> None:
        Base.metadata.drop_all(bind=engine)

    def test_db(self):
        response = client.get("/api/v1/generationtemplate/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, [])
