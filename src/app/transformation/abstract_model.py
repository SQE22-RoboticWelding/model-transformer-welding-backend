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

    def __init__(self, language: str, title: str, version: str):
        self.language = language
        self.title = title
        self.version = version


class Dependee:
    generated_reference: DependeeReference
    initializer: ProgrammingStatement

    def __init__(self, generated_reference: DependeeReference, initializer: ProgrammingStatement):
        self.generated_reference = generated_reference
        self.initializer = initializer


class Setup:
    independent: List[str]
    dependees: List[Dependee]

    def __init__(self, independent: List[str], dependees: List[Dependee]):
        self.independent = independent
        self.dependees = dependees


class ParameterType(Enum):
    STRING = 0
    NUMBER = 1


class NamedParameter:
    abstract_name: str
    generated_name: str
    type: ParameterType
    description: str

    def __init__(self, abstract_name: str, generated_name: str, type: ParameterType, description: str):
        self.abstract_name = abstract_name
        self.generated_name = generated_name
        self.type = type
        self.description = description


class Action:
    abstract_name: str
    generated_name: str
    generated_actor: DependeeReference
    named_parameters: List[NamedParameter]

    def __init__(self,
                 abstract_name: str,
                 generated_name: str,
                 generated_actor: DependeeReference,
                 named_parameters: List[NamedParameter]):
        self.abstract_name = abstract_name
        self.generated_name = generated_name
        self.generated_actor = generated_actor
        self.named_parameters = named_parameters
