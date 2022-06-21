import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.models import create_project, create_welding_point

pytestmark = pytest.mark.asyncio


async def test_create_welding_point_fail(client: AsyncClient, database: AsyncSession):
    data = {
        "project_id": 1,
        "welding_order": 1,
        "name": "P7",
        "description": "Welding point next to the reactor entrance",
        "x": 3.14,
        "y": -5.12,
        "z": 2.4,
        "roll": -1.7,
        "pitch": -2.0,
        "yaw": 4.512
    }
    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=data)
    assert response.status_code == 400


async def test_create_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)

    data = {
        "project_id": project_obj.id,
        "welding_order": 1,
        "name": "P7",
        "description": "Welding point next to the reactor entrance",
        "x": 3.14,
        "y": -5.12,
        "z": 2.4,
        "roll": -1.7,
        "pitch": -2.0,
        "yaw": 4.512
    }
    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["project_id"] == project_obj.id
    assert content["welding_order"] == data["welding_order"]
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["x"] == data["x"]
    assert content["y"] == data["y"]
    assert content["z"] == data["z"]
    assert content["roll"] == data["roll"]
    assert content["pitch"] == data["pitch"]
    assert content["yaw"] == data["yaw"]


async def test_read_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    response = await client.get(f"{settings.API_V1_STR}/weldingpoint/{welding_point_obj.project_id}")
    assert response.status_code == 200

    # Content is a list of welding points
    content = response.json()[0]
    assert "id" in content
    assert content["project_id"] == project_obj.id
    assert content["welding_order"] == welding_point_obj.welding_order
    assert content["name"] == welding_point_obj.name
    assert content["description"] == welding_point_obj.description
    assert content["x"] == welding_point_obj.x
    assert content["y"] == welding_point_obj.y
    assert content["z"] == welding_point_obj.z
    assert content["roll"] == welding_point_obj.roll
    assert content["pitch"] == welding_point_obj.pitch
    assert content["yaw"] == welding_point_obj.yaw


async def test_update_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    data = {"x": 1000.500, "y": -10000}
    response = await client.put(f"{settings.API_V1_STR}/weldingpoint/:id?_id={welding_point_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == welding_point_obj.id
    assert content["x"] == data["x"]
    assert content["y"] == data["y"]


async def test_delete_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    response_delete = await client.delete(f"{settings.API_V1_STR}/weldingpoint/:id?_id={welding_point_obj.id}")
    assert welding_point_obj.as_dict() == response_delete.json()
    assert len(await welding_point.get_multi(db=database)) == 0
