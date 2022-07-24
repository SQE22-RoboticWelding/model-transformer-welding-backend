import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_workpiece import workpiece
from app.tests.utils.models import create_project, create_workpiece

pytestmark = pytest.mark.asyncio


async def test_update_workpiece(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=False)
    workpiece_obj = await create_workpiece(db=database, project_id=project_obj.id, commit_and_refresh=True)

    data = {"position_x": 3.14}
    response = await client.put(f"{settings.API_V1_STR}/workpiece/{workpiece_obj.id}", json=data)
    assert response.status_code == 200

    content = response.json()
    assert content["id"] == workpiece_obj.id
    assert content["position_x"] == data["position_x"]

    workpiece_obj.position_x = data["position_x"]
    workpiece_obj_get = await workpiece.get(db=database, id=workpiece_obj.id)

    assert workpiece_obj_get.project_id == workpiece_obj.project_id
    assert workpiece_obj_get.position_x == workpiece_obj.position_x
    assert workpiece_obj_get.position_y == workpiece_obj.position_y
    assert workpiece_obj_get.position_z == workpiece_obj.position_z
    assert workpiece_obj_get.model_file_name == workpiece_obj.model_file_name
    assert workpiece_obj_get.model_file == workpiece_obj.model_file


async def test_get_model(client: AsyncClient, database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=False)
    workpiece_obj = await create_workpiece(db=database, project_id=project_obj.id, commit_and_refresh=True)

    response = await client.get(f"{settings.API_V1_STR}/workpiece/{workpiece_obj.id}/model")
    assert response.status_code == 200
    assert response.json() == workpiece_obj.model_file
