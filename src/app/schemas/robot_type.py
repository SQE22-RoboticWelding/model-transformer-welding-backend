from typing import Optional
from pydantic import BaseModel

from app.schemas.generation_template import GenerationTemplate, GenerationTemplateBase


class RobotTypeBase(BaseModel):
    id: int
    name: str
    vendor: str
    capacity_load_kg: Optional[float]
    range_m: Optional[float]
    generation_template_id: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "name": "Niryo One",
                "vendor": "Niryo",
                "capacity_load_kg": 50.5,
                "range_m": 3.141
            }
        }


class RobotTypeCreate(RobotTypeBase):
    id: Optional[int]


class RobotTypeUpdate(RobotTypeBase):
    id: Optional[int]
    name: Optional[str]
    vendor: Optional[str]


class RobotTypeWithTemplate(RobotTypeBase):
    generation_template: Optional[GenerationTemplate]

    @staticmethod
    def factory(robot_type: RobotTypeBase, template: GenerationTemplateBase):
        dict_obj = robot_type.as_dict()
        dict_obj["generation_template"] = template.as_dict() if template else None
        return RobotTypeWithTemplate(**dict_obj)


# Properties shared by models stored in DB
class RobotTypeInDBBase(RobotTypeBase):
    class Config:
        orm_mode = True


class RobotType(RobotTypeInDBBase):
    pass


class RobotTypeInDB(RobotTypeInDBBase):
    pass
