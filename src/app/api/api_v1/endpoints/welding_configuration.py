from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.crud.crud_welding_configuration import *
from app.schemas.welding_configuration import *


router = APIRouter()


@router.get("/", response_model=List[WeldingConfiguration])
async def read_welding_configurations(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple welding configuration
    """
    result = await welding_configuration.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=WeldingConfiguration)
async def read_welding_configuration(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve welding configuration by ID
    """
    result = await welding_configuration.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding configuration not found")
    return result


@router.post("/", response_description="Add new welding configuration", response_model=WeldingConfiguration)
async def create_welding_configuration(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_configuration_in: WeldingConfigurationCreate):
    """
    Create new welding configuration
    """
    result = await welding_configuration.create(db=db, obj_in=welding_configuration_in)
    return result


@router.put("/{id}", response_model=WeldingConfiguration)
async def update_welding_configuration(
        *,
        id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_configuration_in: WeldingConfigurationUpdate
) -> Any:
    """
    Update a welding configuration
    """
    result = await welding_configuration.get_by_id(db=db, id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding configuration not found")
    return await welding_configuration.update(db=db, db_obj=result, obj_in=welding_configuration_in)


@router.delete("/{id}", response_model=WeldingConfiguration)
async def delete_welding_configuration(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await welding_configuration.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Welding configuration not found")
    result = await welding_configuration.remove(db=db, obj=result)
    return result
