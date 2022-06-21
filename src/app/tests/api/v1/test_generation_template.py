from datetime import datetime

import pytest
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_robot_type import robot_type
from app.models.robot_type import RobotType
from app.tests.utils.models import get_example_template, create_generation_template

pytestmark = pytest.mark.asyncio


async def test_create_generation_template(client: AsyncClient):
    data = {
        "name": "Test template",
        "description": "Test template description",
        "content": get_example_template()
    }
    response = await client.post(f"{settings.API_V1_STR}/generationtemplate/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["content"] == data["content"]


async def test_read_generation_template(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    response = await client.get(f"{settings.API_V1_STR}/generationtemplate/:id?_id={generation_template_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == generation_template_obj.id
    assert content["description"] == generation_template_obj.description
    assert content["content"] == generation_template_obj.content
    assert datetime.fromisoformat(content["created_at"]) == generation_template_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == generation_template_obj.modified_at


async def test_read_generation_template_not_found(client: AsyncClient):
    response_get = await client.get(f"{settings.API_V1_STR}/generationtemplate/:id?_id=1")
    assert response_get.status_code == 404


async def test_update_generation_template(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    data = {"content": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/generationtemplate/:id?_id={generation_template_obj.id}",
                                json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == generation_template_obj.id
    assert content["content"] == generation_template_obj.content


async def test_delete_robot_type(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    response_delete = await client.delete(f"{settings.API_V1_STR}/generationtemplate/:id?_id={generation_template_obj.id}")
    content = response_delete.json()

    # No dict comparison, as created_at and modified_at is stored as datetime in pydantic Project object and not as
    # string as in the response
    assert content["id"] == generation_template_obj.id
    assert content["description"] == generation_template_obj.description
    assert content["content"] == generation_template_obj.content
    assert datetime.fromisoformat(content["created_at"]) == generation_template_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == generation_template_obj.modified_at

    assert (await robot_type.get(db=database, id=generation_template_obj.id)) is None
