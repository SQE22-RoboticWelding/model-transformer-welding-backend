"""Transformer.py handles transformation of models."""

from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

from app.transformation.instance_model import InstanceModel


templates = Jinja2Templates(directory="app/transformation/templates", keep_trailing_newline=True)


def generate_from_instance_model(instance_model: InstanceModel, request: Request) -> Jinja2Templates.TemplateResponse:
    context = {
        "request": request,
        "model": instance_model
    }
    if instance_model.meta.language == "python3":
        return templates.TemplateResponse("python3.template", context)
    else:
        raise HTTPException(status_code=404, detail=f"Unknown language '{instance_model.meta.language}'.")


class CodeGenerator:
    @staticmethod
    def sequence_to_model(instance_model: InstanceModel, request: Request) -> Jinja2Templates.TemplateResponse:
        context = {
            "request": request,
            "node_name": "default_node",
            "model": instance_model
        }
        return templates.TemplateResponse("python3.template", context)
