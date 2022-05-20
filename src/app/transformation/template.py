from typing import List

from fastapi import HTTPException

from app.schemas.actions.action import Action
from app.schemas.actions.action_parameter import ActionParameter
from app.transformation import abstract_model
from app.transformation import instance_model


class Template:
    meta: abstract_model.MetaInformation
    init: List[List[abstract_model.ProgrammingStatement]]
    setup: abstract_model.Setup
    actions: List[abstract_model.Action]

    @staticmethod
    def instantiate_param(param_definition: abstract_model.NamedParameter, value: object):
        if param_definition.type == abstract_model.ParameterType.STRING:
            return f"\"{value}\""
        elif param_definition.type == abstract_model.ParameterType.NUMBER:
            return f"{value}"
        raise HTTPException(status_code=404, detail=f"Unknown parameter type '{param_definition.type}'.")

    @staticmethod
    def map_param(available_params: List[abstract_model.NamedParameter],
                  target_param: ActionParameter) -> instance_model.NamedParameter:
        for available_param in available_params:
            if target_param.name == available_param.abstract_name:
                param = Template.instantiate_param(available_param, target_param.value)
                return instance_model.NamedParameter(available_param.generated_name, param)

        raise HTTPException(status_code=404, detail=f"Unknown parameter '{target_param.name}'.")

    @staticmethod
    def map_params(available_params: List[abstract_model.NamedParameter],
                   target_params: List[ActionParameter]) -> List[instance_model.NamedParameter]:
        param_instances = []
        for param in target_params:
            mapped_param = Template.map_param(available_params, param)
            param_instances.append(mapped_param)
        return param_instances

    def instantiate_action(self, action: Action) -> instance_model.Action:
        for action_models in self.actions:
            if action_models.abstract_name == action.name:
                parameters = Template.map_params(action_models.named_parameters, action.parameters)

                return instance_model.Action(action_models.generated_name,
                                            action_models.generated_actor,
                                            parameters)
        raise HTTPException(status_code=400, detail=f"Unknown action '{action.name}'.")
