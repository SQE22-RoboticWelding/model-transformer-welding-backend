from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class GenerationTemplateBase(BaseModel):
    id: int
    name: str
    description: Optional[str]
    language: str
    file_extension: str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Niryo One (Python 3, ROS Melodic)",
                "description": "Python 3 templated based on ROS Melodic for the Niryo One",
                "language": "Python 3",
                "file_extension": "py",
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
    language: Optional[str]
    file_extension: Optional[str]
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
