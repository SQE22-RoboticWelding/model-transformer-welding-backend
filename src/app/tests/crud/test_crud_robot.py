import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_robot import robot
from app.models.project import Project
from app.models.robot_type import RobotType
from app.schemas.robot import RobotUpdate
from app.tests.utils.models import create_robot, create_robot_type, create_project

pytestmark = pytest.mark.asyncio


async def test_crud_robot_create_integrity_fail(database: AsyncSession):
    robot_type_obj = RobotType(id=1, name="Test")
    project_obj = Project(id=1, name="Also Test")
    try:
        await create_robot(db=database, robot_type_obj=robot_type_obj)
        assert False
    except IntegrityError:
        assert True


async def test_crud_robot_create(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)

    robot_obj_get = await robot.get(db=database, id=robot_obj.id)
    assert robot_obj.as_dict() == robot_obj_get.as_dict()


async def test_crud_robot_get(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)

    robot_obj_get = await robot.get_by_id(db=database, id=robot_obj.id)
    assert robot_obj.__eq__(robot_obj_get)


async def test_crud_robot_get_multi(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    await create_robot(db=database, robot_type_obj=robot_type_obj)
    await create_robot(db=database, robot_type_obj=robot_type_obj)

    robots = await robot.get_multi(db=database)
    assert len(robots) == 2


async def test_crud_robot_update(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)
    await robot.update(db=database, db_obj=robot_obj, obj_in={"description": "modified"})
    assert robot_obj.description == "modified"

    await robot.update(db=database, db_obj=robot_obj, obj_in=RobotUpdate(description="modified again"))
    assert robot_obj.description == "modified again"


async def test_crud_robot_delete(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    robot_obj = await create_robot(db=database, robot_type_obj=robot_type_obj)

    result = await robot.remove(db=database, obj=robot_obj)
    assert robot_obj.as_dict() == result.as_dict()

    result = await robot.get(db=database, id=robot_obj.id)
    assert result is None
