from typing import Optional
from pydantic import BaseModel
from pydantic.schema import datetime


class ProjectBase(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Death Star",
                "description": "Project for the Death Star"
            }
        }


class ProjectCreate(ProjectBase):
    id: Optional[int]


class ProjectUpdate(ProjectBase):
    id: Optional[int]
    name: Optional[str]


# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


class Project(ProjectInDBBase):
    pass


class ProjectInDB(ProjectInDBBase):
    pass
