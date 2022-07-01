import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_robot_type import robot_type
from app.schemas.robot_type import RobotTypeUpdate
from app.tests.utils.models import create_robot_type, create_generation_template

pytestmark = pytest.mark.asyncio


async def test_crud_robot_type_create(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    robot_type_obj_get = await robot_type.get(db=database, id=robot_type_obj.id)
    assert robot_type_obj.as_dict() == robot_type_obj_get.as_dict()


async def test_crud_robot_type_create_with_template(database: AsyncSession):
    generation_template_obj = await create_generation_template(db=database)
    robot_type_obj = await create_robot_type(db=database, template_id=generation_template_obj.id)
    robot_type_obj_get = await robot_type.get(db=database, id=robot_type_obj.id)
    assert robot_type_obj.as_dict() == robot_type_obj_get.as_dict()


async def test_crud_robot_type_get(database: AsyncSession):
    robot_type_obj = await create_robot_type(db=database)
    robot_type_obj_get = await robot_type.get_by_id(db=database, id=robot_type_obj.id)
    assert robot_type_obj.__eq__(robot_type_obj_get)


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
    assert robot_type_obj.as_dict() == result.as_dict()

    result = await robot_type.get(db=database, id=robot_type_obj.id)
    assert result is None
