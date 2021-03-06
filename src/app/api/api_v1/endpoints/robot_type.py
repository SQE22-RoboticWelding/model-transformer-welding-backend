from fastapi import Depends, HTTPException

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_robot_type import *
from app.schemas.robot_type import *


router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[RobotTypeWithTemplate])
async def read_robot_types(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple robot types
    """
    robot_types = await robot_type.get_multi(db=db, skip=skip, limit=limit)
    robot_type_with_template = [RobotTypeWithTemplate.factory(obj, obj.generation_template) for obj in robot_types]
    return robot_type_with_template


@router.get("/{robot_type_id}", response_model=RobotTypeWithTemplate)
async def read_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_id: int
) -> Any:
    """
    Retrieve robot type by ID
    """
    robot_type_obj = await robot_type.get_by_id(db=db, id=robot_type_id)
    if not robot_type_obj:
        raise HTTPException(status_code=404, detail="Robot type not found")
    return RobotTypeWithTemplate.factory(robot_type_obj, robot_type_obj.generation_template)


@router.post("/", response_description="Add new robot type", response_model=RobotType)
async def create_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_in: RobotTypeCreate):
    """
    Create new robot type
    """
    result = await robot_type.create(db=db, obj_in=robot_type_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.put("/{robot_type_id}", response_model=RobotType)
async def update_robot_type(
        *,
        robot_type_id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_in: RobotTypeUpdate
) -> Any:
    """
    Update a robot type
    """
    robot_type_obj = await robot_type.get_by_id(db=db, id=robot_type_id)
    if not robot_type_obj:
        raise HTTPException(status_code=404, detail="Robot type not found")

    result = await robot_type.update(db=db, db_obj=robot_type_obj, obj_in=robot_type_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{robot_type_id}", response_model=RobotType)
async def delete_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_id: int
) -> Any:
    robot_type_obj = await robot_type.get_by_id(db=db, id=robot_type_id)
    if not robot_type_obj:
        raise HTTPException(status_code=404, detail="Robot type not found")
    if len(robot_type_obj.robots) > 0:
        raise HTTPException(status_code=420, detail="Robot type has existing robots. Please delete first")

    result = await robot_type.remove(db=db, obj=robot_type_obj)
    await db.commit()
    return result
