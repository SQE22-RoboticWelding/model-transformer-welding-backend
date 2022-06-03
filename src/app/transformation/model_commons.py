"""
Classes commonly used in the different model abstraction layers.
"""
from abc import ABC
from enum import Enum
from typing import TypeVar

from pydantic import BaseModel


class ParameterType(Enum):
    STRING = "string"
    NUMBER = "number"


DataType = TypeVar("DataType", str, float)


class MetaInformation(BaseModel):
    language: str
    title: str
    version: str


class AbstractBase(BaseModel, ABC):
    abstract_name: str


class GenerationBase(BaseModel, ABC):
    generated_name: str
