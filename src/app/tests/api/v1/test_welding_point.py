import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_welding_point import welding_point
from app.tests.utils.models import create_project, create_welding_point,get_welding_point_json_data

pytestmark = pytest.mark.asyncio


async def test_create_welding_point_integrity_fail(client: AsyncClient):
    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=get_welding_point_json_data())
    assert response.status_code == 400


async def test_create_welding_point_welding_order_fail(client: AsyncClient, database: AsyncSession):
    await create_project(db=database, commit_and_refresh=True)

    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=get_welding_point_json_data())
    assert response.status_code == 200
    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=get_welding_point_json_data())
    assert response.status_code == 420


async def test_create_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    data = get_welding_point_json_data()

    response = await client.post(f"{settings.API_V1_STR}/weldingpoint/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["project_id"] == project_obj.id
    assert content["welding_order"] == data["welding_order"]
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["x_original"] == data["x_original"]
    assert content["y_original"] == data["y_original"]
    assert content["z_original"] == data["z_original"]
    assert content["x"] == data["x"]
    assert content["y"] == data["y"]
    assert content["z"] == data["z"]
    assert content["roll"] == data["roll"]
    assert content["pitch"] == data["pitch"]
    assert content["yaw"] == data["yaw"]

    assert (await welding_point.get(db=database, id=content["id"])).as_dict() == content


async def test_read_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj, commit_and_refresh=True)
    await database.refresh(project_obj)

    response = await client.get(f"{settings.API_V1_STR}/weldingpoint/{welding_point_obj.project_id}")
    assert response.status_code == 200

    # Content is a list of welding points
    content = response.json()[0]
    assert "id" in content
    assert content["project_id"] == project_obj.id
    assert content["welding_order"] == welding_point_obj.welding_order
    assert content["name"] == welding_point_obj.name
    assert content["description"] == welding_point_obj.description
    assert content["x_original"] == welding_point_obj.x_original
    assert content["y_original"] == welding_point_obj.y_original
    assert content["z_original"] == welding_point_obj.z_original
    assert content["x"] == welding_point_obj.x
    assert content["y"] == welding_point_obj.y
    assert content["z"] == welding_point_obj.z
    assert content["roll"] == welding_point_obj.roll
    assert content["pitch"] == welding_point_obj.pitch
    assert content["yaw"] == welding_point_obj.yaw


async def test_read_welding_point_not_found(client: AsyncClient):
    response = await client.get(f"{settings.API_V1_STR}/weldingpoint/1")
    assert response.status_code == 404


async def test_update_welding_point_welding_order_fail(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    await create_welding_point(db=database, project_obj=project_obj, welding_order_in=0)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj, welding_order_in=1,
                                                   commit_and_refresh=True)

    data = {"welding_order": 0}
    response = await client.put(f"{settings.API_V1_STR}/weldingpoint/{welding_point_obj.id}", json=data)
    assert response.status_code == 420


async def test_update_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj, commit_and_refresh=True)

    data = {
        "x": welding_point_obj.x_original - welding_point_obj.tolerance / 10,
        "y": welding_point_obj.x_original + welding_point_obj.tolerance / 10
    }
    response = await client.put(f"{settings.API_V1_STR}/weldingpoint/{welding_point_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == welding_point_obj.id
    assert content["x"] == data["x"]
    assert content["y"] == data["y"]

    welding_point_obj.x = data["x"]
    welding_point_obj.y = data["y"]
    assert (await welding_point.get(db=database, id=welding_point_obj.id)).as_dict() == welding_point_obj.as_dict()


async def test_delete_welding_point(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj, commit_and_refresh=True)

    response_delete = await client.delete(f"{settings.API_V1_STR}/weldingpoint/{welding_point_obj.id}")
    assert response_delete.status_code == 200

    assert welding_point_obj.as_dict() == response_delete.json()
    assert len(await welding_point.get_multi(db=database)) == 0
