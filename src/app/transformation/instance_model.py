from typing import List

from app.transformation import abstract_model as AbstractModel
from app.transformation.template import Template


class NamedParameter:
    generated_name: str
    value_representation: str

    def __init__(self, generated_name: str, value_representation: str):
        self.generated_name = generated_name
        self.value_representation = value_representation


class Action:
    generated_name: str
    generated_actor: AbstractModel.DependeeReference
    parameters: List[NamedParameter]

    def __init__(self, generated_name: str, generated_actor: AbstractModel.DependeeReference,
                 parameters: List[NamedParameter]):
        self.generated_name = generated_name
        self.generated_actor = generated_actor
        self.parameters = parameters


class InstanceModel:
    meta: AbstractModel.MetaInformation
    init: List[List[AbstractModel.ProgrammingStatement]]
    setup: AbstractModel.Setup
    actions: List[Action]

    def __init__(self,
                 meta: AbstractModel.MetaInformation,
                 init: List[List[AbstractModel.ProgrammingStatement]],
                 setup: AbstractModel.Setup,
                 actions: List[Action]):
        self.meta = meta
        self.init = init
        self.setup = setup
        self.actions = actions


def create_instance_model(template: Template, abstract_actions: List[AbstractModel.Action]):
    instance_actions: List[Action] = []
    for abstract_action in abstract_actions:
        instance_action = template.instantiate_action(abstract_action)
        instance_actions.append(instance_action)

    return InstanceModel(template.meta, template.init, template.setup, instance_actions)
