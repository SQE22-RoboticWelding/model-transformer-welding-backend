import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.models import create_robot_type, create_robot

pytestmark = pytest.mark.asyncio


async def test_create_robot_fail(client: AsyncClient):
    data = {"robot_type_id": 1, "description": "Test"}
    response = await client.post(f"{settings.API_V1_STR}/robot/", json=data)
    assert response.status_code == 400


async def test_create_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    data = {"robot_type_id": robot_type_obj.id, "description": "Test"}
    response = await client.post(f"{settings.API_V1_STR}/robot/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["description"] == data["description"]
    assert content["robot_type_id"] == data["robot_type_id"]


async def test_read_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)
    response = await client.get(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_obj.id
    assert content["description"] == robot_obj.description
    assert content["robot_type_id"] == robot_obj.robot_type_id


async def test_update_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)
    data = {"description": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_obj.id
    assert content["description"] == data["description"]


async def test_delete_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)
    await client.delete(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}")
    response = await client.get(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}")
    assert response.status_code == 404