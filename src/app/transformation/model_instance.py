"""
Classes defining the instance of a low-code model.
They combine the abstract model and the template of a target platform.
Based on these instance classes, code can be generated.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.transformation.model_commons import GenerationBase, DataType
from app.transformation.model_lowcode import ModelLowCode
from app.transformation.template import Template


class ParameterInstance(GenerationBase):
    value: DataType


class ActionInstance(GenerationBase):
    generated_actor: Optional[str]
    parameters: List[ParameterInstance]


class ModelInstance(BaseModel):
    template: Template
    model_lowcode: ModelLowCode
    action_instances: List[ActionInstance]
