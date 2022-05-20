from typing import List, Optional

from fastapi import HTTPException

from app.schemas.actions.Action import Action
from app.schemas.actions.ActionParameter import ActionParameter
from app.transformation import AbstractModel
from app.transformation import InstanceModel


class Template:
    meta: AbstractModel.MetaInformation
    init: List[List[AbstractModel.ProgrammingStatement]]
    setup: AbstractModel.Setup
    actions: List[AbstractModel.Action]

    @staticmethod
    def map_param(available_params: List[AbstractModel.NamedParameter],
                  target_param: ActionParameter) -> InstanceModel.NamedParameter:
        for available_param in available_params:
            if target_param.name == available_param.abstract_name:
                return InstanceModel.NamedParameter(available_param.generated_name, target_param.value)
        raise HTTPException(status_code=400, detail=f"Unknown parameter '{target_param.name}'.")

    @staticmethod
    def map_params(available_params: List[AbstractModel.NamedParameter],
                   target_params: List[ActionParameter]) -> List[InstanceModel.NamedParameter]:
        param_instances = []
        for param in target_params:
            mapped_param = Template.map_param(available_params, param)
            param_instances.append(mapped_param)
        return param_instances

    def instantiate_action(self, action: Action) -> InstanceModel.Action:
        for action_models in self.actions:
            if action_models.abstract_name == action.name:
                parameters = Template.map_params(action_models.named_parameters, action.parameters)

                return InstanceModel.Action(action_models.generated_name,
                                            action_models.generated_actor,
                                            parameters)
        raise HTTPException(status_code=400, detail=f"Unknown action '{action.name}'.")
