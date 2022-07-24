from typing import Optional, List
from pydantic import BaseModel
from pydantic.schema import datetime

from app.schemas.workpiece import WorkpieceBase, WorkpieceCreate
from app.schemas.welding_point import WeldingPointBase
from app.schemas.workpiece import WorkpieceBase


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
    workpiece: Optional[WorkpieceCreate]


class ProjectUpdate(ProjectBase):
    id: Optional[int]
    name: Optional[str]


class ProjectWithData(ProjectBase):
    created_at: datetime
    modified_at: datetime
    welding_points: List[WeldingPointBase]
    workpiece: Optional[WorkpieceBase]

    @staticmethod
    def factory(project: ProjectBase, welding_points: List[WeldingPointBase], workpiece: WorkpieceBase = None):
        dict_obj = project.as_dict()
        dict_obj["welding_points"] = [obj.as_dict() for obj in welding_points]

        if workpiece is not None:
            dict_obj["workpiece"] = workpiece.as_dict()
        return ProjectWithData(**dict_obj)


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
