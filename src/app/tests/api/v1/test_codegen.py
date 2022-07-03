import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.tests.utils.models import create_project, create_generation_template, create_welding_point

pytestmark = pytest.mark.asyncio


async def test_codegen(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    project_id = project_obj.id

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    generation_template_obj = await create_generation_template(db=database, commit_and_refresh=True)
    await database.refresh(welding_point_obj)

    generation_template_id = generation_template_obj.id

    data = {"generation_template_id": project_id, "project_id": generation_template_id}
    response = await client.post(f"{settings.API_V1_STR}/codegeneration/generate", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content == f"{welding_point_obj.x}, {welding_point_obj.y}, {welding_point_obj.z} / " \
                      f"{welding_point_obj.roll}, {welding_point_obj.pitch}, {welding_point_obj.yaw} / " \
                      f"{welding_point_obj.welding_order}"
