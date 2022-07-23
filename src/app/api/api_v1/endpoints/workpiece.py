from typing import Any

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_project import project
from app.crud.crud_workpiece import workpiece as crud_workpiece
from app.schemas.workpiece import Workpiece, WorkpieceUpdate

router = APIRouterWithGenericExceptionHandler()


@router.get("/{workpiece_id}/model", response_model=str)
async def get_model(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        workpiece_id: int
) -> Any:
    """
    Retrieve workpiece model by project ID
    """
    workpiece_obj = await crud_workpiece.get_by_id(db=db, id=workpiece_id)
    if not workpiece_obj:
        raise HTTPException(status_code=404, detail="Workpiece not found")
    return workpiece_obj.model_file


@router.put("/{workpiece_id}", response_model=Workpiece)
async def update_workpiece(
        *,
        workpiece_id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        workpiece_in: WorkpieceUpdate
) -> Any:
    """
    Update a workpiece
    """
    workpiece_obj = await crud_workpiece.get_by_id(db=db, id=workpiece_id)
    result = await crud_workpiece.update(db=db, db_obj=workpiece_obj, obj_in=workpiece_in)
    await db.commit()
    await db.refresh(result)
    return result
