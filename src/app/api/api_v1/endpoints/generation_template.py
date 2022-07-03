from fastapi import Depends, HTTPException
from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_generation_template import *
from app.schemas.generation_template import *


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


@router.get("/{id}", response_model=GenerationTemplate)
async def read_generation_template(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    """
    Retrieve generation template by ID
    """
    result = await generation_template.get_by_id(db=db, id=_id)
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


@router.put("/{id}", response_model=GenerationTemplate)
async def update_generation_template(
        *,
        _id: int,
        db: AsyncSession = Depends(deps.get_async_db),
        generation_template_in: GenerationTemplateUpdate
) -> Any:
    """
    Update a generation template
    """
    generation_template_obj = await generation_template.get_by_id(db=db, id=_id)
    if not generation_template_obj:
        raise HTTPException(status_code=404, detail="Generation template not found")

    result = await generation_template.update(db=db, db_obj=generation_template_obj, obj_in=generation_template_in)
    await db.commit()
    await db.refresh(result)
    return result


@router.delete("/{id}", response_model=GenerationTemplate)
async def delete_generation_template(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        _id: int
) -> Any:
    result = await generation_template.get_by_id(db=db, id=_id)
    if not result:
        raise HTTPException(status_code=404, detail="Generation template not found")

    result = await generation_template.remove(db=db, obj=result)
    await db.commit()
    return result
