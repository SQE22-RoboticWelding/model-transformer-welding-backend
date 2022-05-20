"""Transformer.py handles transformation of models."""

from fastapi import Request
from fastapi.templating import Jinja2Templates

from app.transformation.InstanceModel import InstanceModel

templates = Jinja2Templates(directory="app/transformation/templates", keep_trailing_newline=True)


def generate_from_instance_model(instance_model: InstanceModel, request: Request) -> Jinja2Templates.TemplateResponse:
    context = {
        "request": request,
        "model": instance_model
    }
    return templates.TemplateResponse("python3.template", context)


class Transformer:
    @staticmethod
    def sequence_to_model(instance_model: InstanceModel, request: Request) -> Jinja2Templates.TemplateResponse:
        context = {
            "request": request,
            "node_name": "default_node",
            "model": instance_model
        }
        return templates.TemplateResponse("python3.template", context)
