from typing import List

from app.schemas.actions import action
from app.transformation import abstract_model
from app.transformation import template


class InstanceModel:
    meta: abstract_model.MetaInformation
    init: List[List[abstract_model.ProgrammingStatement]]
    setup: abstract_model.Setup
    actions: List[template.Action]

    def __init__(self,
                 meta: abstract_model.MetaInformation,
                 init: List[List[abstract_model.ProgrammingStatement]],
                 setup: abstract_model.Setup,
                 actions: List[template.Action]):
        self.meta = meta
        self.init = init
        self.setup = setup
        self.actions = actions


def create_instance_model(temp: template.Template, abstract_actions: List[action.Action]):
    instance_actions: List[template.Action] = []
    for abstract_action in abstract_actions:
        instance_action = temp.instantiate_action(abstract_action)
        instance_actions.append(instance_action)

    return InstanceModel(temp.meta, temp.init, temp.setup, instance_actions)
