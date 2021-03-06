import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.crud.crud_welding_point import welding_point
from app.crud.crud_project import project
from app.schemas.welding_point import WeldingPointUpdate
from app.tests.utils.models import create_welding_point, create_project, get_welding_point_create

pytestmark = pytest.mark.asyncio


async def test_crud_welding_point_create_integrity_fail(database: AsyncSession):
    project_obj = Project(id=1, name="Test")
    try:
        await create_welding_point(db=database, project_obj=project_obj)
        assert False
    except IntegrityError:
        assert True


async def test_crud_welding_point_create(database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    welding_point_obj_get = await welding_point.get(db=database, id=welding_point_obj.id)
    assert welding_point_obj.as_dict() == welding_point_obj_get.as_dict()


async def test_crud_welding_point_create_multi(database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_points = [get_welding_point_create(project_obj=project_obj),
                      get_welding_point_create(project_obj=project_obj),
                      get_welding_point_create(project_obj=project_obj)]

    created_welding_points = await welding_point.create_multi(db=database, obj_in=welding_points)
    assert len(created_welding_points) == 3


async def test_crud_welding_point_get(database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    welding_point_obj_get = await welding_point.get_by_id(db=database, id=welding_point_obj.id)
    assert welding_point_obj.__eq__(welding_point_obj_get)


async def test_crud_welding_point_get_multi(database: AsyncSession):
    project_obj = await create_project(db=database)
    await create_welding_point(db=database, project_obj=project_obj)
    await create_welding_point(db=database, project_obj=project_obj)
    welding_points = await welding_point.get_multi(db=database)
    assert len(welding_points) == 2


async def test_crud_welding_point_update(database: AsyncSession):
    project_obj = await create_project(db=database)

    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)
    await welding_point.update(db=database, db_obj=welding_point_obj, obj_in={"name": "modified"})
    assert welding_point_obj.name == "modified"

    await welding_point.update(db=database, db_obj=welding_point_obj, obj_in=WeldingPointUpdate(name="modified again"))
    assert welding_point_obj.name == "modified again"


async def test_crud_welding_point_delete(database: AsyncSession):
    project_obj = await create_project(db=database)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)

    result = await welding_point.remove(db=database, obj=welding_point_obj)
    assert welding_point_obj.as_dict() == result.as_dict()

    result = await welding_point.get(db=database, id=welding_point_obj.id)
    assert result is None


async def test_crud_welding_point_delete_cascade(database: AsyncSession):
    project_obj = await create_project(db=database)
    welding_point_obj = await create_welding_point(db=database, project_obj=project_obj)

    result = await project.remove(db=database, obj=project_obj)
    assert isinstance(result, Project)

    result = await welding_point.get(db=database, id=welding_point_obj.id)
    assert result is None
