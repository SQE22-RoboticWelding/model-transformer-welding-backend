from typing import List, Optional

from fastapi import HTTPException

from app.schemas.actions import action
from app.schemas.actions.action_parameter import ActionParameter
from app.transformation import abstract_model


class NamedParameter:
    generated_name: str
    value_representation: str

    def __init__(self, generated_name: str, value_representation: str):
        self.generated_name = generated_name
        self.value_representation = value_representation


class Action:
    generated_name: str
    generated_actor: Optional[abstract_model.DependeeReference]
    parameters: List[NamedParameter]

    def __init__(self, generated_name: str, generated_actor: abstract_model.DependeeReference,
                 parameters: List[NamedParameter]):
        self.generated_name = generated_name
        self.generated_actor = generated_actor
        self.parameters = parameters


class Template:
    meta: abstract_model.MetaInformation
    init: List[List[abstract_model.ProgrammingStatement]]
    setup: abstract_model.Setup
    actions: List[abstract_model.Action]

    def __init__(self,
                 meta: abstract_model.MetaInformation,
                 init: List[List[abstract_model.ProgrammingStatement]],
                 setup: abstract_model.Setup,
                 actions: List[abstract_model.Action]):
        self.meta = meta
        self.init = init
        self.setup = setup
        self.actions = actions

    @staticmethod
    def instantiate_param(param_definition: abstract_model.NamedParameter, value: object):
        if param_definition.type == abstract_model.ParameterType.STRING:
            return f"'{value}'"
        elif param_definition.type == abstract_model.ParameterType.NUMBER:
            return f"{value}"
        raise HTTPException(status_code=404, detail=f"Unknown parameter type '{param_definition.type}'.")

    @staticmethod
    def map_param(available_params: List[abstract_model.NamedParameter],
                  target_param: ActionParameter) -> NamedParameter:
        for available_param in available_params:
            if target_param.name == available_param.abstract_name:
                param = Template.instantiate_param(available_param, target_param.value)
                return NamedParameter(available_param.generated_name, param)

        raise HTTPException(status_code=404, detail=f"Unknown parameter '{target_param.name}'.")

    @staticmethod
    def map_params(available_params: List[abstract_model.NamedParameter],
                   target_params: List[ActionParameter]) -> List[NamedParameter]:
        param_instances = []
        for param in target_params:
            mapped_param = Template.map_param(available_params, param)
            param_instances.append(mapped_param)
        return param_instances

    def instantiate_action(self, act: action.Action) -> Action:
        for action_models in self.actions:
            if action_models.abstract_name == act.name:
                parameters = Template.map_params(action_models.named_parameters, act.parameters)

                return Action(action_models.generated_name, action_models.generated_actor, parameters)
        raise HTTPException(status_code=400, detail=f"Unknown action '{act.name}'.")
