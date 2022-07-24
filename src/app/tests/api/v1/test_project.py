from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.models import create_project
from app.crud.crud_project import project
from app.schemas.welding_point import WeldingPoint
from testdata.getter import get_file
from testdata.validation import validate_project_file_welding_points

pytestmark = pytest.mark.asyncio


async def test_read_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    response = await client.get(f"{settings.API_V1_STR}/project/{project_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == project_obj.id
    assert content["name"] == project_obj.name
    assert content["description"] == project_obj.description
    assert datetime.fromisoformat(content["created_at"]) == project_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == project_obj.modified_at


async def test_read_project_not_found(client: AsyncClient):
    response_get = await client.get(f"{settings.API_V1_STR}/project/1")
    assert response_get.status_code == 404


async def test_update_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    data = {"description": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/project/{project_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == project_obj.id

    project_obj.description = data["description"]
    project_obj_get = await project.get(db=database, id=project_obj.id)

    assert project_obj_get.description == project_obj.description
    assert project_obj_get.name == project_obj.name
    assert project_obj_get.created_at == project_obj.created_at
    assert project_obj_get.modified_at >= project_obj.modified_at


async def test_delete_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    response_delete = await client.delete(f"{settings.API_V1_STR}/project/{project_obj.id}")
    assert response_delete.status_code == 200
    content = response_delete.json()

    # No dict comparison, as created_at and modified_at is stored as datetime in pydantic Project object and not as
    # string as in the response
    assert content["id"] == project_obj.id
    assert content["name"] == project_obj.name
    assert content["description"] == project_obj.description
    assert datetime.fromisoformat(content["created_at"]) == project_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == project_obj.modified_at

    assert (await project.get(db=database, id=project_obj.id)) is None


async def test_upload_project(client: AsyncClient, database: AsyncSession):
    file = get_file(filename="project_file.xlsx")

    response = await client.post(f"{settings.API_V1_STR}/project/upload?name=testproject", files={'file': file})
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["name"] == "testproject"

    welding_points = [WeldingPoint(**obj) for obj in content["welding_points"]]
    validate_project_file_welding_points(welding_points)

    project_obj = await project.get_by_id(db=database, id=content["id"])
    validate_project_file_welding_points(project_obj.welding_points)
