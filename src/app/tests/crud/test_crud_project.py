import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.crud.crud_project import project
from app.schemas.project import ProjectUpdate
from app.tests.utils.models import create_project

pytestmark = pytest.mark.asyncio


async def test_crud_project_create(database: AsyncSession):
    project_obj = await create_project(db=database)
    assert project_obj is not None
    assert isinstance(project_obj, Project)


async def test_crud_project_get(database: AsyncSession):
    project_obj = await create_project(db=database)
    tmp = await project.get_by_id(db=database, id=project_obj.id)
    assert project_obj.__eq__(tmp)


async def test_crud_project_get_multi(database: AsyncSession):
    await create_project(db=database)
    await create_project(db=database)
    projects = await project.get_multi(db=database)
    assert len(projects) == 2


async def test_crud_project_update(database: AsyncSession):
    project_obj = await create_project(db=database)
    await project.update(db=database, db_obj=project_obj, obj_in={"name": "modified"})
    assert project_obj.name == "modified"

    await project.update(db=database, db_obj=project_obj, obj_in=ProjectUpdate(name="modified again"))
    assert project_obj.name == "modified again"
