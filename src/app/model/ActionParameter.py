"""ActionParameter.py describes the parameter of an action a robot takes."""

from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ActionParameter(Generic[T], BaseModel):
    name: str = ""
    value: T = None

    def __init__(self, name: str, value: T):
        super().__init__()
        self.name = name
        self.value = value
