from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class GenerationTemplateBase(BaseModel):
    name: str
    description: Optional[str]
    content: str


class GenerationTemplateCreate(GenerationTemplateBase):
    pass


class GenerationTemplateUpdate(GenerationTemplateBase):
    name: Optional[str]
    description: Optional[str]
    content: Optional[str]


# Properties shared by models stored in DB
class GenerationTemplateInDBBase(GenerationTemplateBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


class GenerationTemplate(GenerationTemplateInDBBase):
    pass


class GenerationTemplateInDB(GenerationTemplateInDBBase):
    pass
