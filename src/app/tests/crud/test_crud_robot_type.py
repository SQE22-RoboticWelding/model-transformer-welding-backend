import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.robot_type import RobotType
from app.crud.crud_robot_type import robot_type
from app.schemas.robot_type import RobotTypeUpdate
from app.tests.utils.models import create_robot_type

pytestmark = pytest.mark.asyncio


async def test_crud_robot_type_create(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    assert robot_type_obj is not None
    assert isinstance(robot_type_obj, RobotType)


async def test_crud_robot_type_get(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    tmp = await robot_type.get_by_id(db=database, id=robot_type_obj.id)
    assert robot_type_obj.__eq__(tmp)


async def test_crud_robot_type_get_multi(database: AsyncSession):
    await create_robot_type(db=database)
    await create_robot_type(db=database)
    robot_types = await robot_type.get_multi(db=database)
    assert len(robot_types) == 2


async def test_crud_robot_type_update(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    await robot_type.update(db=database, db_obj=robot_type_obj, obj_in={"name": "modified"})
    assert robot_type_obj.name == "modified"

    await robot_type.update(db=database, db_obj=robot_type_obj, obj_in=RobotTypeUpdate(name="modified again"))
    assert robot_type_obj.name == "modified again"


async def test_crud_robot_type_delete(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)

    result = await robot_type.remove(db=database, obj=robot_type_obj)
    assert isinstance(result, RobotType)

    result = await robot_type.get(db=database, id=robot_type_obj.id)
    assert result is None
