import json
from enum import Enum
from typing import List

from pydantic import BaseModel


ProgrammingStatement = str
DependeeReference = str


class MetaInformation(BaseModel):
    language: str
    title: str
    version: str


class Dependee(BaseModel):
    generated_reference: DependeeReference
    initializer: ProgrammingStatement


class Setup(BaseModel):
    independent: List[str]
    dependees: List[Dependee]


class ParameterType(Enum):
    STRING = "string"
    NUMBER = "number"


class NamedParameter(BaseModel):
    abstract_name: str
    generated_name: str
    type: ParameterType
    description: str


class Action(BaseModel):
    abstract_name: str
    generated_name: str
    generated_actor: DependeeReference
    named_parameters: List[NamedParameter]
