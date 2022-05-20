"""Action.py describes the action a robot takes."""

from typing import List

from app.schemas.actions.ActionParameter import ActionParameter


class Action:
    name: str = ""
    parameters: List[ActionParameter] = []

    def __init__(self, name: str, parameters: List[ActionParameter]):
        super().__init__()
        self.name = name
        self.parameters = parameters
