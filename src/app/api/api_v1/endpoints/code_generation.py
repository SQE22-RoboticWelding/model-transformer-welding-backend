from typing import Any
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_generation_template import generation_template
from app.crud.crud_welding_configuration import welding_configuration
from app.codegen.code_generator import CodeGenerator


router = APIRouterWithGenericExceptionHandler()


class RequestBodyGenerate(BaseModel):
    generation_template_id: int
    welding_configuration_id: int


@router.post("/generate", response_class=PlainTextResponse)
async def generate(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        body: RequestBodyGenerate
) -> Any:
    """
    Generate code by manually passing in welding points
    """
    result_template = await generation_template.get_by_id(db=db, id=body.generation_template_id)
    result_welding_configuration = await welding_configuration.get_by_id(db=db, id=body.welding_configuration_id)
    if not result_template:
        raise HTTPException(status_code=404, detail="Generation template not found")
    elif not result_welding_configuration:
        raise HTTPException(status_code=404, detail="Welding configuration not found")
    else:
        result = CodeGenerator.generate(result_template, result_welding_configuration)
        return result
