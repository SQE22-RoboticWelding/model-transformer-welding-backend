from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class GenerationTemplateBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    content: str

    schema_extra = {
        "example": {
            "name": "Niryo One (Python 3, ROS Melodic)",
            "description": "Python 3 templated based on ROS Melodic for the Niryo One",
            "content":
                "{% for p in welding_points %}"
                "{{p.x}}, {{p.y}}, {{p.z}} / {{p.roll}}, {{p.pitch}}, {{p.yaw}} / {{p.welding_order}}"
                "{% endfor %}"
        }
    }


class GenerationTemplateCreate(GenerationTemplateBase):
    id: Optional[int]


class GenerationTemplateUpdate(GenerationTemplateBase):
    id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    content: Optional[str]


# Properties shared by models stored in DB
class GenerationTemplateInDBBase(GenerationTemplateBase):
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


class GenerationTemplate(GenerationTemplateInDBBase):
    pass


class GenerationTemplateInDB(GenerationTemplateInDBBase):
    pass
