from typing import Any, Dict
from fastapi import APIRouter, HTTPException
from app.crud.crud_generation_template import generation_template
from app.codegen.code_generator import CodeGenerator


router = APIRouter()


@router.post("/manual-welding-points", response_model=str, deprecated=True)
async def generate(
        *,
        generation_template_id: int,
        values: Dict
) -> Any:
    """
    Generate code by manually passing in welding points
    """
    result = await generation_template.get_by_id(generation_template_id)
    if not result:
        raise HTTPException(status_code=404, detail="Generation template not found")
    else:
        return CodeGenerator.generate(result, values)
