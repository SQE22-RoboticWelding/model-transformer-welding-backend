from fastapi import Depends, HTTPException, UploadFile
from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_welding_configuration import *
from app.crud.crud_welding_point import *
from app.parser.pandas_parser import PandasParser
from app.schemas.welding_configuration import *


router = APIRouterWithGenericExceptionHandler()


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


@router.post("/upload", response_description="Upload file to create a new welding configuration",
             response_model=WeldingConfiguration)
async def upload_welding_configuration(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        name: str,
        file: UploadFile
) -> Any:
    parser = PandasParser(file)
    if not parser.validate():
        raise HTTPException(status_code=415, detail="File is not valid")

    content = await file.read()
    parse_result = parser.parse(content)
    if parse_result.error:
        raise HTTPException(status_code=415, detail=parse_result.detail)

    # Create new welding configuration
    welding_configuration_create = WeldingConfigurationCreate(name=name)
    welding_configuration_obj = await welding_configuration.create(db=db, obj_in=welding_configuration_create)
    if welding_configuration_obj is None:
        raise HTTPException(status_code=500, detail="Could not create new welding configuration")

    # Create welding points
    result = await welding_point.create_multi(
        db=db, obj_in=parser.get_welding_points(welding_configuration=welding_configuration_obj))
    if result is None:
        raise HTTPException(status_code=500, detail="Could not create welding point")

    return welding_configuration_obj


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
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        welding_configuration_in: WeldingConfigurationUpdate
) -> Any:
    """
    Update a welding configuration
    """
    result = await welding_configuration.get_by_id(db=db, id=_id)
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
