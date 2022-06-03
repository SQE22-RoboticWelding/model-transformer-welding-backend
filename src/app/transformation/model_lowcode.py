"""
Classes defining the abstract model in a low-code environment.
This means meta information and the abstractly described sequence of actions.
"""
from typing import List

from pydantic import BaseModel

from app.transformation.model_commons import MetaInformation, AbstractBase, DataType


class ParameterLowCode(AbstractBase):
    value: DataType


class ActionLowCode(AbstractBase):
    parameters: List[ParameterLowCode]


class ModelLowCode(BaseModel):
    meta: MetaInformation
    actions: List[ActionLowCode]
