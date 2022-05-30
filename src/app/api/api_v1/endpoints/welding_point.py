from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.crud.crud_welding_point import *
from app.schemas.welding_point import *


router = APIRouter()


@router.get("/", response_model=List[WeldingPoint])
async def read_welding_points(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple robot types
    """
    result = await welding_point.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=WeldingPoint)
async def read_welding_point(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve robot type by ID
    """
    result = await welding_point.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding point not found")
    return result


@router.post("/", response_description="Add new welding point", response_model=WeldingPoint)
async def create_welding_point(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_point_in: WeldingPointCreate):
    """
    Create new robot type
    """
    result = await welding_point.create(db=db, obj_in=welding_point_in)
    return result


@router.put("/{id}", response_model=WeldingPoint)
async def update_welding_point(
        *,
        id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_point_in: WeldingPointUpdate
) -> Any:
    """
    Update a robot type
    """
    result = await welding_point.get_by_id(db=db, id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding point not found")
    return await welding_point.update(db=db, db_obj=result, obj_in=welding_point_in)


@router.delete("/{id}", response_model=WeldingPoint)
async def delete_welding_point(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await welding_point.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding point not found")
    result = await welding_point.remove(db=db, obj=result)
    return result
