import json
from enum import Enum
from typing import List


ProgrammingStatement = str
DependeeReference = str


class Serializable:
    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class MetaInformation:
    language: str
    title: str
    version: str


class Dependee:
    generated_reference: DependeeReference
    initializer: ProgrammingStatement


class Setup:
    independent: List[str]
    dependees: List[Dependee]


class ParameterType(Enum):
    STRING = 0
    NUMBER = 1


class NamedParameter:
    abstract_name: str
    generated_name: str
    type: ParameterType
    description: str


class Action:
    abstract_name: str
    generated_name: str
    generated_actor: DependeeReference
    named_parameters: List[NamedParameter]
