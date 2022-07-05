from datetime import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_generation_template import generation_template
from app.crud.crud_robot_type import robot_type
from app.tests.utils.models import get_example_template, create_generation_template

pytestmark = pytest.mark.asyncio


async def test_create_generation_template(client: AsyncClient, database: AsyncSession):
    data = {
        "name": "Test template",
        "description": "Test template description",
        "content": get_example_template(),
        "language": "HolyC",
        "file_extension": ".HC"
    }
    response = await client.post(f"{settings.API_V1_STR}/generationtemplate/", json=data)
    assert response.status_code == 200

    content = response.json()
    assert "id" in content
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["content"] == data["content"]
    assert content["language"] == data["language"]
    assert content["file_extension"] == data["file_extension"]

    generation_template_obj_get = await generation_template.get(db=database, id=content["id"])
    assert generation_template_obj_get.name == content["name"]
    assert generation_template_obj_get.description == content["description"]
    assert generation_template_obj_get.content == content["content"]
    assert generation_template_obj_get.language == content["language"]
    assert generation_template_obj_get.file_extension == content["file_extension"]


async def test_read_generation_template(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database, commit_and_refresh=True)
    response = await client.get(f"{settings.API_V1_STR}/generationtemplate/{generation_template_obj.id}")
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == generation_template_obj.id
    assert content["description"] == generation_template_obj.description
    assert content["content"] == generation_template_obj.content
    assert content["language"] == generation_template_obj.language
    assert content["file_extension"] == generation_template_obj.file_extension
    assert datetime.fromisoformat(content["created_at"]) == generation_template_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == generation_template_obj.modified_at


async def test_read_generation_template_not_found(client: AsyncClient):
    response_get = await client.get(f"{settings.API_V1_STR}/generationtemplate/1")
    assert response_get.status_code == 404


async def test_update_generation_template(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database, commit_and_refresh=True)
    data = {"content": "modified"}
    response = await client.put(f"{settings.API_V1_STR}/generationtemplate/{generation_template_obj.id}",
                                json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == generation_template_obj.id
    assert content["content"] == data["content"]

    generation_template_obj.content = data["content"]
    generation_template_obj_get = await generation_template.get(db=database, id=generation_template_obj.id)

    assert generation_template_obj_get.content == generation_template_obj.content
    assert generation_template_obj_get.name == generation_template_obj.name
    assert generation_template_obj_get.description == generation_template_obj.description
    assert generation_template_obj_get.language == generation_template_obj.language
    assert generation_template_obj_get.file_extension == generation_template_obj.file_extension
    assert generation_template_obj_get.created_at == generation_template_obj.created_at
    assert generation_template_obj_get.modified_at >= generation_template_obj.modified_at


async def test_delete_generation_template(client: AsyncClient, database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database, commit_and_refresh=True)
    response_delete = await client\
        .delete(f"{settings.API_V1_STR}/generationtemplate/{generation_template_obj.id}")
    assert response_delete.status_code == 200
    content = response_delete.json()

    # No dict comparison, as created_at and modified_at is stored as datetime in pydantic Project object and not as
    # string as in the response
    assert content["id"] == generation_template_obj.id
    assert content["description"] == generation_template_obj.description
    assert content["content"] == generation_template_obj.content
    assert content["language"] == generation_template_obj.language
    assert content["file_extension"] == generation_template_obj.file_extension
    assert datetime.fromisoformat(content["created_at"]) == generation_template_obj.created_at
    assert datetime.fromisoformat(content["modified_at"]) == generation_template_obj.modified_at

    assert (await generation_template.get(db=database, id=generation_template_obj.id)) is None
