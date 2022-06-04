"""
Classes defining the instance of a low-code model.
They combine the abstract model and the generation_config of a target platform.
Based on these instance classes, code can be generated.
"""
from typing import List, Optional

from pydantic import BaseModel

from app.transformation.model_commons import GenerationBase, DataType
from app.transformation.model_lowcode import ModelLowCode
from app.transformation.generation_config import GenerationConfig


class ParameterInstance(GenerationBase):
    value: DataType


class ActionInstance(GenerationBase):
    generated_actor: Optional[str]
    parameters: List[ParameterInstance]


class ModelInstance(BaseModel):
    template: GenerationConfig
    model_lowcode: ModelLowCode
    action_instances: List[ActionInstance]
