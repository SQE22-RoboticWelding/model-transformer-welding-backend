from fastapi import Depends, HTTPException

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_robot import *
from app.schemas.robot import *


router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[Robot])
async def read_robots(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple robots
    """
    result = await robot.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=Robot)
async def read_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve robot by ID
    """
    result = await robot.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot not found")
    return result


@router.post("/", response_description="Add new robot", response_model=Robot)
async def create_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_in: RobotCreate):
    """
    Create new robot
    """
    result = await robot.create(db=db, obj_in=robot_in)
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
    result = await robot.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot not found")
    return await robot.update(db=db, db_obj=result, obj_in=robot_in)


@router.delete("/{id}", response_model=Robot)
async def delete_robot(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await robot.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot not found")
    result = await robot.remove(db=db, obj=result)
    return result
