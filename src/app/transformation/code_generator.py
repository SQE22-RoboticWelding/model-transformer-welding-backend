"""code_generator.py handles transformation of models."""
from typing import List

from fastapi import Request, HTTPException
from fastapi.templating import Jinja2Templates

from app.transformation.model_commons import DataType, ParameterType
from app.transformation.model_instance import ParameterInstance, ActionInstance
from app.transformation.model_lowcode import ParameterLowCode, ActionLowCode
from app.transformation.template import ParameterTemplate, ActionTemplate, Template

templates = Jinja2Templates(directory="app/transformation/templates", keep_trailing_newline=True)


class CodeGenerator:
    @staticmethod
    def instantiate_param(param_template: ParameterTemplate, value: DataType) -> str:
        if param_template.type == ParameterType.STRING:
            return f"\"{value}\""
        elif param_template.type == ParameterType.NUMBER:
            return f"{value}"

        raise HTTPException(status_code=404, detail=f"Unknown parameter type '{param_template.type}'.")

    @staticmethod
    def map_param(param_templates: List[ParameterTemplate], value: ParameterLowCode) -> ParameterInstance:
        for param_template in param_templates:
            if value.abstract_name == param_template.abstract_name:
                param = CodeGenerator.instantiate_param(param_template, value.value)
                return ParameterInstance(generated_name=param_template.generated_name, value=param)

        raise HTTPException(status_code=404, detail=f"Unknown parameter '{value.abstract_name}'.")

    @staticmethod
    def instantiate_action(action: ActionLowCode, action_templates: List[ActionTemplate]) -> ActionInstance:
        for action_template in action_templates:
            if action.abstract_name == action_template.abstract_name:
                parameters = [CodeGenerator.map_param(action_template.parameters, param)
                              for param in action.parameters]
                return ActionInstance(generated_name=action_template.generated_name,
                                      generated_actor=action_template.generated_actor,
                                      parameters=parameters)

        raise HTTPException(status_code=404, detail=f"Unknown action '{action.abstract_name}'.")

    @staticmethod
    def generate(template: Template, actions_lowcode: List[ActionLowCode],
                 request: Request) -> Jinja2Templates.TemplateResponse:
        actions = [CodeGenerator.instantiate_action(alc, template.actions) for alc in actions_lowcode]
        context = {
            "request": request,
            "model": {
                "setup": template.setup,
                "init": template.init,
                "actions": actions
            }
        }
        if template.meta.language == "python3":
            return templates.TemplateResponse("python3.jinja", context)
        else:
            raise HTTPException(status_code=404, detail=f"Unknown language '{template.meta.language}'.")
