import pytest
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.api.deps import get_sync_db
from app.db.base import Base


# SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()
#
#
# app.dependency_overrides[get_sync_db] = override_get_db
# client = TestClient(app)
#
#
# class RobotTypeTest(unittest.TestCase):
#     def setUp(self) -> None:
#         Base.metadata.create_all(bind=engine)
#
#     def tearDown(self) -> None:
#         Base.metadata.drop_all(bind=engine)
#
#     @pytest.fixture()
#     def test_db(self):
#         response = client.get("/robottype/")
#         self.assertEqual(response, [])
