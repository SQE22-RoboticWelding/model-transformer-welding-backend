"""
Classes defining the template in a low-code environment.
The template is the descriptor by which any abstract model can be translated into a target platform's language.
"""
from typing import List

from pydantic import BaseModel

from app.transformation.model_commons import MetaInformation, AbstractBase, GenerationBase, ParameterType


ProgrammingStatement = str
DependeeReference = str


class Dependee(GenerationBase):
    initializer: ProgrammingStatement


class Setup(BaseModel):
    independent: List[ProgrammingStatement]
    dependees: List[Dependee]


class ParameterTemplate(AbstractBase, GenerationBase):
    type: ParameterType
    description: str


class ActionTemplate(AbstractBase, GenerationBase):
    generated_actor: DependeeReference
    parameters: List[ParameterTemplate]


class Template(BaseModel):
    meta: MetaInformation
    init: List[List[ProgrammingStatement]]
    setup: Setup
    actions: List[ActionTemplate]
