from typing import Any
from fastapi import APIRouter, HTTPException
from app.crud.crud_generation_template import generation_template
from app.crud.crud_welding_configuration import welding_configuration
from app.codegen.code_generator import CodeGenerator


router = APIRouter()


@router.post("/manual-welding-points", response_model=str, deprecated=True)
async def generate(
        *,
        generation_template_id: int,
        welding_configuration_id: int
) -> Any:
    """
    Generate code by manually passing in welding points
    """
    gen_template = await generation_template.get_by_id(generation_template_id)
    welding_config = await welding_configuration.get_by_id(welding_configuration_id)
    if not gen_template:
        raise HTTPException(status_code=404, detail="Generation template not found")
    elif not welding_config:
        raise HTTPException(status_code=404, detail="Welding configuration not found")
    else:
        return CodeGenerator.generate(generation_template, welding_config)
