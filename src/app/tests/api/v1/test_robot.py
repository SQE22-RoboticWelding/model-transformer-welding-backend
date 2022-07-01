import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_robot import robot
from app.tests.utils.models import create_robot_type, create_robot, create_project

pytestmark = pytest.mark.asyncio


async def test_create_robot_integrity_fail(client: AsyncClient):
    data = {"robot_type_id": 1, "description": "Test"}
    response = await client.post(f"{settings.API_V1_STR}/robot/", json=data)
    assert response.status_code == 400


@pytest.mark.skip(reason="issue with database cursors and lazy loading")
async def test_create_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    project_obj = await create_project(db=database)

    data = {"robot_type_id": robot_type_obj.id,
            "project_id": project_obj.id,
            "name": "Scratchy",
            "description": "Test",
            "position_x": 5,
            "position_y": 5.5,
            "position_z": 5.55,
            "position_norm_vector_x": 0,
            "position_norm_vector_y": 0.5,
            "position_norm_vector_z": 0.75}
    response = await client.post(f"{settings.API_V1_STR}/robot/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["robot_type_id"] == data["robot_type_id"]
    assert content["project_id"] == data["project_id"]
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["position_x"] == data["position_x"]
    assert content["position_y"] == data["position_y"]
    assert content["position_z"] == data["position_z"]
    assert content["position_norm_vector_x"] == data["position_norm_vector_x"]
    assert content["position_norm_vector_y"] == data["position_norm_vector_y"]
    assert content["position_norm_vector_z"] == data["position_norm_vector_z"]

    assert (await robot.get(db=database, id=content["id"])).as_dict() == content


@pytest.mark.skip(reason="issue with database cursors and lazy loading")
async def test_read_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    project_obj = await create_project(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj, project_obj=project_obj)
    response = await client.get(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_obj.id
    assert content["robot_type_id"] == robot_obj.robot_type_id
    assert content["project_id"] == robot_obj.project_id
    assert content["robot_type"] == robot_type_obj.as_dict()
    assert content["name"] == robot_obj.name
    assert content["description"] == robot_obj.description
    assert content["position_x"] == robot_obj.position_x
    assert content["position_y"] == robot_obj.position_y
    assert content["position_z"] == robot_obj.position_z
    assert content["position_norm_vector_x"] == robot_obj.position_norm_vector_x
    assert content["position_norm_vector_y"] == robot_obj.position_norm_vector_y
    assert content["position_norm_vector_z"] == robot_obj.position_norm_vector_z


async def test_read_robot_not_found(client: AsyncClient):
    response_get = await client.get(f"{settings.API_V1_STR}/robot/:id?_id=1")
    assert response_get.status_code == 404


@pytest.mark.skip(reason="issue with database cursors and lazy loading")
async def test_update_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    project_obj = await create_project(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj, project_obj=project_obj)
    data = {"description": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == robot_obj.id
    assert content["description"] == data["description"]

    robot_obj.description = data["description"]
    assert (await robot.get(db=database, id=robot_obj.id)).as_dict() == robot_obj.as_dict()


@pytest.mark.skip(reason="issue with database cursors and lazy loading")
async def test_delete_robot(client: AsyncClient, database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    project_obj = await create_project(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj, project_obj=project_obj)
    response_delete = await client.delete(f"{settings.API_V1_STR}/robot/:id?_id={robot_obj.id}")
    assert response_delete.status_code == 200

    assert robot_obj.as_dict() == response_delete.json()
    assert (await robot.get(db=database, id=robot_obj.id)) is None
