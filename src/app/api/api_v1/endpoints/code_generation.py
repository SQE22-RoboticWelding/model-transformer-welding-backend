from typing import Any
from fastapi import HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler
from app.crud.crud_generation_template import generation_template
from app.crud.crud_project import project
from app.codegen.code_generator import CodeGenerator


router = APIRouterWithGenericExceptionHandler()


class RequestBodyGenerate(BaseModel):
    generation_template_id: int
    project_id: int


@router.post("/generate", response_model=str, deprecated=True)
async def generate(
        *,
        db: AsyncSession = Depends(deps.get_async_db),
        body: RequestBodyGenerate
) -> Any:
    """
    Generate code by manually passing in welding points
    """
    result_template = await generation_template.get_by_id(db=db, id=body.generation_template_id)
    result_project = await project.get_by_id(db=db, id=body.project_id)
    if not result_template:
        raise HTTPException(status_code=404, detail="Generation template not found")
    elif not result_project:
        raise HTTPException(status_code=404, detail="Project not found")
    else:
        result = CodeGenerator.generate(result_template, result_project)
        return result
