from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.codegen.predefined_templates import PredefinedTemplates
from app.crud.crud_generation_template import generation_template
from app.schemas.generation_template import GenerationTemplateCreate


router = APIRouterWithGenericExceptionHandler()


@router.get("/test/{id}")
async def test(id):
    return {"message": f"{id} was sent"}


@router.get("/database")
async def database(
        db: AsyncSession = Depends(deps.get_async_db)
):
    if db:
        return {"message": "Database reachable"}
    else:
        return {"message": "Database not reachable"}


@router.post("/init-predefined")
async def init_predefined(
        db: AsyncSession = Depends(deps.get_async_db)
):
    template = GenerationTemplateCreate(name="NiryoOne-ROS Predefined",
                                        description="Predefined template for python api niryo_one_ros",
                                        content=PredefinedTemplates.NIRYO_ONE_ROS)
    return await generation_template.create(db, template)
