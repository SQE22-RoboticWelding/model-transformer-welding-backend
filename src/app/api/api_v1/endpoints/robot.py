from fastapi import Depends, HTTPException

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_robot import *
from app.schemas.robot import *


router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[RobotWithType])
async def read_robots(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple robots
    """
    robots = await robot.get_multi(db=db, skip=skip, limit=limit)

    robots_with_type = [RobotWithType.factory(obj, obj.robot_type) for obj in robots]
    return robots_with_type


@router.get("/{id}", response_model=RobotWithType)
async def read_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve robot by ID
    """
    robot_obj = await robot.get_by_id(db=db, id=_id)
    if not robot_obj:
        raise HTTPException(status_code=404, detail="Robot not found")

    return RobotWithType.factory(robot_obj, robot_obj.robot_type)


@router.post("/", response_description="Add new robot", response_model=Robot)
async def create_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_in: RobotCreate):
    """
    Create new robot
    """
    result = await robot.create(db=db, obj_in=robot_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.put("/{id}", response_model=Robot)
async def update_robot(
        *,
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_in: RobotUpdate
) -> Any:
    """
    Update a robot
    """
    robot_obj = await robot.get_by_id(db=db, id=_id)
    if not robot_obj:
        raise HTTPException(status_code=404, detail="Robot not found")

    result = await robot.update(db=db, db_obj=robot_obj, obj_in=robot_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{id}", response_model=Robot)
async def delete_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    robot_obj = await robot.get_by_id(db=db, id=_id)
    if not robot_obj:
        raise HTTPException(status_code=404, detail="Robot not found")

    result = await robot.remove(db=db, obj=robot_obj)
    await db.commit()
    return result
