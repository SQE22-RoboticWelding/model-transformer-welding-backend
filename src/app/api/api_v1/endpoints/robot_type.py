from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.crud.crud_robot_type import *
from app.schemas.robot_type import *


router = APIRouter()


@router.get("/", response_model=List[RobotType])
async def read_robot_types(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple robot types
    """
    result = await robot_type.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=RobotType)
async def read_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve robot type by ID
    """
    result = await robot_type.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot type not found")
    return result


@router.post("/", response_description="Add new robot type", response_model=RobotType)
async def create_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_in: RobotTypeCreate):
    """
    Create new robot type
    """
    result = await robot_type.create(db=db, obj_in=robot_type_in)
    return result


@router.put("/{id}", response_model=RobotType)
async def update_robot_type(
        *,
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        robot_type_in: RobotTypeUpdate
) -> Any:
    """
    Update a robot type
    """
    result = await robot_type.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot type not found")
    return await robot_type.update(db=db, db_obj=result, obj_in=robot_type_in)


@router.delete("/{id}", response_model=RobotType)
async def delete_robot_type(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await robot_type.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Robot type not found")
    result = await robot_type.remove(db=db, obj=result)
    return result
