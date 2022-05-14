"""Action.py describes the action a robot takes."""

from typing import List

from pydantic import BaseModel

from model.ActionParameter import ActionParameter


class Action(BaseModel):
    key: str = ""
    parameters: List[ActionParameter] = []

    def __init__(self, key: str, parameters: List[ActionParameter]):
        super().__init__()
        self.key = key
        self.parameters = parameters
