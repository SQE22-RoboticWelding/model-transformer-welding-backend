import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_project import project
from app.schemas.project import ProjectUpdate
from app.tests.utils.models import create_project

pytestmark = pytest.mark.asyncio


async def test_crud_project_create(database: AsyncSession):
    project_obj = await create_project(db=database)
    project_obj_get = await project.get(db=database, id=project_obj.id)
    assert project_obj.as_dict() == project_obj_get.as_dict()


async def test_crud_project_get(database: AsyncSession):
    project_obj = await create_project(db=database)
    project_obj_get = await project.get_by_id(db=database, id=project_obj.id)
    assert project_obj.__eq__(project_obj_get)


async def test_crud_project_get_multi(database: AsyncSession):
    await create_project(db=database)
    await create_project(db=database)
    projects = await project.get_multi(db=database)
    assert len(projects) == 2


async def test_crud_project_update(database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)
    await project.update(db=database, db_obj=project_obj, obj_in={"name": "modified"})
    assert project_obj.name == "modified"

    await database.refresh(project_obj)
    await project.update(db=database, db_obj=project_obj, obj_in=ProjectUpdate(name="modified again"))
    assert project_obj.name == "modified again"


async def test_crud_project_delete(database: AsyncSession):
    project_obj = await create_project(db=database, commit_and_refresh=True)

    result = await project.remove(db=database, obj=project_obj)
    assert project_obj.as_dict() == result.as_dict()

    result = await project.get(db=database, id=project_obj.id)
    assert result is None
