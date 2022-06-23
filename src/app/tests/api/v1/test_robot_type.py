import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_robot_type import robot_type
from app.tests.utils.models import create_robot_type

pytestmark = pytest.mark.asyncio


async def test_create_robot_type(client: AsyncClient, database: AsyncSession):
    data = {"name": "Niryo Ten", "vendor": "Niryo", "capacity_load_kg": 10.512, "range_m": 5120}
    response = await client.post(f"{settings.API_V1_STR}/robottype/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["name"] == data["name"]
    assert content["vendor"] == data["vendor"]
    assert content["capacity_load_kg"] == data["capacity_load_kg"]
    assert content["range_m"] == data["range_m"]
    assert "id" in content

    assert (await robot_type.get(db=database, id=content["id"])).as_dict() == content


async def test_read_robot_type(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    response = await client.get(f"{settings.API_V1_STR}/robottype/:id?_id={robot_type_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_type_obj.id
    assert content["name"] == robot_type_obj.name
    assert content["vendor"] == robot_type_obj.vendor
    assert content["capacity_load_kg"] == robot_type_obj.capacity_load_kg
    assert content["range_m"] == robot_type_obj.range_m


async def test_read_robot_type_not_found(client: AsyncClient):
    response_get = await client.get(f"{settings.API_V1_STR}/robottype/:id?_id=1")
    assert response_get.status_code == 404


async def test_update_robot_type(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    data = {"name": "Niryo Twenty", "range_m": 4000}
    response = await client.put(f"{settings.API_V1_STR}/robottype/:id?_id={robot_type_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_type_obj.id
    assert content["name"] == data["name"]
    assert content["range_m"] == data["range_m"]

    robot_type_obj.name = data["name"]
    robot_type_obj.range_m = data["range_m"]
    assert (await robot_type.get(db=database, id=robot_type_obj.id)).as_dict() == robot_type_obj.as_dict()


async def test_delete_robot_type(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    response_delete = await client.delete(f"{settings.API_V1_STR}/robottype/:id?_id={robot_type_obj.id}")
    assert response_delete.status_code == 200

    assert robot_type_obj.as_dict() == response_delete.json()
    assert (await robot_type.get(db=database, id=robot_type_obj.id)) is None
