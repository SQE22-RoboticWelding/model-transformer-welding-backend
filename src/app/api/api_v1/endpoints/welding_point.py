from fastapi import Depends, HTTPException
from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_welding_point import *
from app.crud.crud_project import *
from app.schemas.welding_point import *


router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[WeldingPoint])
async def read_welding_points(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple welding points
    """
    result = await welding_point.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{project_id}",
            response_description="Welding points belonging to a project",
            response_model=List[WeldingPoint])
async def read_welding_point(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_id: int
) -> Any:
    """
    Retrieve list of welding points belonging to a project
    """
    project_obj = await project.get_by_id(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_obj.welding_points


@router.post("/", response_description="Add new welding point", response_model=WeldingPoint)
async def create_welding_point(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_point_in: WeldingPointCreate):
    """
    Create new welding point
    """
    result = await welding_point.create(db=db, obj_in=welding_point_in)
    return result


@router.put("/{id}", response_model=WeldingPoint)
async def update_welding_point(
        *,
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_point_in: WeldingPointUpdate
) -> Any:
    """
    Update a welding point
    """
    result = await welding_point.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding point not found")
    return await welding_point.update(db=db, db_obj=result, obj_in=welding_point_in)


@router.put("/", response_model=List[WeldingPoint])
async def update_welding_points(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_points_in: List[WeldingPointUpdate]
) -> Any:
    """
    Update multiple welding points. ID is then required in the WeldingPointUpdate
    """
    # Check, if each element has a proper ID
    if any(wp.id is None for wp in welding_points_in):
        raise HTTPException(status_code=400,
                            detail="To update multiple welding points each element needs to contain its ID")

    updates = []
    for wp in welding_points_in:
        element = await welding_point.get_by_id(db=db, id=wp.id)
        updates.append(await welding_point.update(db=db, db_obj=element, obj_in=wp))

    return updates


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
