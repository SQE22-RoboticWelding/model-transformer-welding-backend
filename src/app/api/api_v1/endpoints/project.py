from fastapi import Depends, HTTPException, UploadFile
from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_project import *
from app.crud.crud_welding_point import *
from app.parser.pandas_parser import PandasParser
from app.schemas.project import *


router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[Project])
async def read_project(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple projects
    """
    result = await project.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/{id}", response_model=Project)
async def read_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve project by ID
    """
    result = await project.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@router.post("/upload", response_description="Upload file to create a new project",
             response_model=Project)
async def upload_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        name: str,
        file: UploadFile
) -> Any:
    """
    Create new project by uploading a file
    """
    parser = PandasParser(file)
    if not parser.validate():
        raise HTTPException(status_code=415, detail="File is not valid")

    content = await file.read()
    parse_result = parser.parse(content)
    if parse_result.error:
        raise HTTPException(status_code=415, detail=parse_result.detail)

    # Create new project
    project_create = ProjectCreate(name=name)
    project_obj = await project.create(db=db, obj_in=project_create)
    if project_obj is None:
        raise HTTPException(status_code=500, detail="Could not create new project")

    # Create welding points
    result = await welding_point.create_multi(
        db=db, obj_in=parser.get_welding_points(project=project_obj))
    if result is None:
        raise HTTPException(status_code=500, detail="Could not create welding point")

    return project_obj


@router.post("/", response_description="Add new project", response_model=Project)
async def create_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_in: ProjectCreate):
    """
    Create new project
    """
    result = await project.create(db=db, obj_in=project_in)
    return result


@router.put("/{id}", response_model=Project)
async def update_project(
        *,
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        project_in: ProjectUpdate
) -> Any:
    """
    Update a project
    """
    result = await project.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return await project.update(db=db, db_obj=result, obj_in=project_in)


@router.delete("/{id}", response_model=Project)
async def delete_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await project.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    result = await project.remove(db=db, obj=result)
    return result