from typing import List

from pydantic import BaseModel

from app.schemas.actions import action
from app.transformation import abstract_model
from app.transformation import template


class InstanceModel(BaseModel):
    meta: abstract_model.MetaInformation
    init: List[List[abstract_model.ProgrammingStatement]]
    setup: abstract_model.Setup
    actions: List[template.Action]


def create_instance_model(temp: template.Template, abstract_actions: List[action.Action]):
    instance_actions: List[template.Action] = []
    for abstract_action in abstract_actions:
        instance_action = temp.instantiate_action(abstract_action)
        instance_actions.append(instance_action)

    return InstanceModel(meta=temp.meta, init=temp.init, setup=temp.setup, actions=instance_actions)
