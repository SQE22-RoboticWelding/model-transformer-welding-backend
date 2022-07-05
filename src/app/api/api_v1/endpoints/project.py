from fastapi import Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler

from app.codegen.code_generator import zip_generated_code, generate_code_by_robot
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


@router.get("/{project_id}", response_model=Project)
async def read_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_id: int
) -> Any:
    """
    Retrieve project by ID
    """
    result = await project.get_by_id(db=db, id=project_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return result


@router.get("/{id}/generate", response_description="Zip file containing the generated code")
async def generate_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """"
    Generate and retrieve code of the project
    """
    project_obj = await project.get_by_id(db=db, id=_id)
    if project_obj is None:
        raise HTTPException(status_code=404, detail="Project not found")

    # Get welding points seperated by robot, each list sorted by welding order ascending
    wp_by_robot = []
    robots = {wp.robot_id for wp in project_obj.welding_points}
    for robot_id in robots:
        wps = [wp for wp in project_obj.welding_points if wp.robot_id == robot_id]
        wps.sort(key=lambda x: x.welding_order)
        wp_by_robot.append(wps)

    # Generate code for each robot
    generated_code = generate_code_by_robot(wp_by_robot)

    # Create in-memory zip with generated code
    zip_obj = zip_generated_code(generated_code)

    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"{project_obj.name}_{current_time}.zip"
    return StreamingResponse(zip_obj,
                             media_type="application/zip",
                             headers={"Content-Disposition": f"attachment;filename={zip_name}"})


@router.post("/upload", response_description="Upload file to create a new project",
             response_model=ProjectWithData)
async def upload_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        name: str,
        description: Optional[str] = None,
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
    project_create = ProjectCreate(name=name, description=description)
    project_obj = await project.create(db=db, obj_in=project_create)
    if project_obj is None:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not create new project")

    # Create welding points
    welding_points = await welding_point.create_multi(
        db=db, obj_in=parser.get_welding_points(project=project_obj))
    if welding_points is None:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Could not create welding points")

    await db.commit()
    await db.refresh(project_obj)
    return ProjectWithData.factory(project_obj, project_obj.welding_points)


@router.post("/", response_description="Add new project", response_model=Project)
async def create_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_in: ProjectCreate):
    """
    Create new project
    """
    result = await project.create(db=db, obj_in=project_in)

    await db.commit()
    await db.refresh(result)
    return result


@router.put("/{project_id}", response_model=Project)
async def update_project(
        *,
        project_id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        project_in: ProjectUpdate
) -> Any:
    """
    Update a project
    """
    project_obj = await project.get_by_id(db=db, id=project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="Project not found")

    result = await project.update(db=db, db_obj=project_obj, obj_in=project_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{project_id}", response_model=Project)
async def delete_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_id: int
) -> Any:
    project_obj = await project.get_by_id(db=db, id=project_id)
    if not project_obj:
        await db.rollback()
        raise HTTPException(status_code=404, detail="Project not found")

    result = await project.remove(db=db, obj=project_obj)
    await db.commit()
    return result
