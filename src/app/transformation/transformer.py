"""Transformer.py handles transformation of models."""

from fastapi import Request
from fastapi.templating import Jinja2Templates

from model.ActionSequence import ActionSequence


templates = Jinja2Templates(directory="templates", keep_trailing_newline=True)


class Transformer:

    # TODO: replace with permanent solution also taking templates
    @staticmethod
    def sequence_to_model(sequence: ActionSequence, request: Request) -> Jinja2Templates.TemplateResponse:
        context = {
            "request": request,
            "node_name": "default_node",
            "action_sequence": sequence.dict()['actions']
        }
        return templates.TemplateResponse("niryo_one_ros.template.py", context)
