from fastapi import Depends, HTTPException
from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.api.api_v1.endpoints.utils import verifications
from app.crud.crud_generation_template import *
from app.models.robot_type import RobotType
from app.schemas.generation_template import *
from app.templates.getter import get_library_templates

router = APIRouterWithGenericExceptionHandler()


@router.get("/", response_model=List[GenerationTemplate])
async def read_generation_templates(
        db: AsyncSession = Depends(deps.get_async_db),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve multiple generation templates
    """
    result = await generation_template.get_multi(db=db, skip=skip, limit=limit)
    return result


@router.get("/librarytemplates", response_model=List[LibraryTemplate])
async def read_library_templates() -> Any:
    """
    Retrieve all pre-defined templates from the template library
    """
    return get_library_templates()


@router.get("/{generation_template_id}", response_model=GenerationTemplate)
async def read_generation_template(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        generation_template_id: int
) -> Any:
    """
    Retrieve generation template by ID
    """
    result = await generation_template.get_by_id(db=db, id=generation_template_id)
    if not result:
        raise HTTPException(status_code=404, detail="Generation template not found")
    return result


@router.post("/", response_description="Add new generation template", response_model=GenerationTemplate)
async def create_generation_template(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        generation_template_in: GenerationTemplateCreate):
    """
    Create new generation template
    """
    result = await generation_template.create(db=db, obj_in=generation_template_in)

    await db.commit()
    await db.refresh(result)
    return result


@router.put("/{generation_template_id}", response_model=GenerationTemplate)
async def update_generation_template(
        *,
        generation_template_id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        generation_template_in: GenerationTemplateUpdate
) -> Any:
    """
    Update a generation template
    """
    generation_template_obj = await generation_template.get_by_id(db=db, id=generation_template_id)
    if not generation_template_obj:
        raise HTTPException(status_code=404, detail="Generation template not found")

    if not verifications.verify_template_version_increase_on_content_change(
            generation_template_obj, generation_template_in):
        raise HTTPException(status_code=420, detail="Template content changed without increasing the version")

    result = await generation_template.update(db=db, db_obj=generation_template_obj, obj_in=generation_template_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{generation_template_id}", response_model=GenerationTemplate)
async def delete_generation_template(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        generation_template_id: int
) -> Any:
    """
    Delete a generation template
    """
    generation_template_obj = await generation_template.get_by_id(db=db, id=generation_template_id)
    if not generation_template_obj:
        raise HTTPException(status_code=404, detail="Generation template not found")

    # Check, that template is not used in any robot type
    linked_robot_types = await db.execute(select(RobotType)
                                          .filter(RobotType.generation_template_id == generation_template_obj.id))
    linked_robot_types = linked_robot_types.scalars().all()
    if len(linked_robot_types) > 0:
        robot_types_name = [rt.name for rt in linked_robot_types]
        raise HTTPException(status_code=420,
                            detail=f"The template is still used as template for robot types {robot_types_name}")

    result = await generation_template.remove(db=db, obj=generation_template_obj)
    await db.commit()
    return result
