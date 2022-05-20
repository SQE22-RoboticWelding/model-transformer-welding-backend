"""action_parameter.py describes the parameter of an action a robot takes."""

from typing import Generic, TypeVar


T = TypeVar("T")


class ActionParameter(Generic[T]):
    name: str = ""
    value: T = None

    def __init__(self, name: str, value: T):
        super().__init__()
        self.name = name
        self.value = value
