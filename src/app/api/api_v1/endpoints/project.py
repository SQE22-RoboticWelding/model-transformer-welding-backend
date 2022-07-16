from fastapi import Depends, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.codegen.code_generator import CodeGenerator
from app.crud.crud_project import *
from app.crud.crud_welding_point import *
from app.parser.pandas_parser import PandasParser
from app.schemas.project import *
from app.api.api_v1.endpoints.utils import verifications


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


@router.get("/{project_id}/generate", response_description="Zip file containing the generated code")
async def generate_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_id: int
) -> Any:
    """"
    Generate and retrieve code of the project
    """
    project_obj = await project.get_by_id(db=db, id=project_id)
    validate_project_for_generation(project_obj)

    generated_code = CodeGenerator.generate_code_for_project(project_obj)

    # Create in-memory zip with generated code
    zip_obj = CodeGenerator.zip_generated_code(generated_code)

    current_time = datetime.now().strftime("%Y%m%d-%H%M%S")
    zip_name = f"{project_obj.name}_{current_time}.zip"
    return StreamingResponse(zip_obj,
                             media_type="application/zip",
                             headers={"Content-Disposition": f"attachment;filename={zip_name}"})


@router.get("/{project_id}/generate/validate", status_code=204)
async def validate_generate_project(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        project_id: int
) -> Any:
    project_obj = await project.get_by_id(db=db, id=project_id)
    validate_project_for_generation(project_obj)
    CodeGenerator.generate_code_for_project(project_obj)


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

    if not verifications.verify_welding_coordinates_in_tolerance(welding_points):
        await db.rollback()
        raise HTTPException(status_code=420,
                            detail="Update on welding point does not ensure that the coordinates are within the"
                                   "given tolerance")

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


def validate_project_for_generation(project_obj: Project):
    if project_obj is None:
        raise HTTPException(status_code=404, detail="Project not found")

    if not verifications.verify_welding_points_robot_assignment(project_obj=project_obj):
        raise HTTPException(status_code=420, detail="Not all welding points have a robot assigned")

    if not verifications.verify_project_robot_type_template_assignment(project_obj=project_obj):
        raise HTTPException(status_code=420, detail="Not all used robot types of robots have a generation "
                                                    "template assigned")
