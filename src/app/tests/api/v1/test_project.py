from datetime import datetime
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.models import create_project

pytestmark = pytest.mark.asyncio


async def test_create_project(client: AsyncClient):
    data = {"name": "Test", "description": "Test description"}
    response = await client.post(f"{settings.API_V1_STR}/project/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "created_at" in content
    assert "modified_at" in content


async def test_read_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    response = await client.get(f"{settings.API_V1_STR}/project/:id?_id={project_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == project_obj.id
    assert content["name"] == project_obj.name
    assert content["description"] == project_obj.description
    assert datetime.fromisoformat(content["created_at"]) == project_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == project_obj.modified_at


async def test_update_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    data = {"description": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/project/:id?_id={project_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == project_obj.id
    assert content["description"] == "modified"


async def test_delete_project(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database)
    await client.delete(f"{settings.API_V1_STR}/project/:id?_id={project_obj.id}")
    response = await client.get(f"{settings.API_V1_STR}/project/:id?_id={project_obj.id}")
    assert response.status_code == 404
