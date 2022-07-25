from typing import Optional
from pydantic import BaseModel


class WorkpieceBase(BaseModel):
    id: int
    project_id: int
    model_file_name: Optional[str]
    position_x: Optional[float]
    position_y: Optional[float]
    position_z: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "project_id": 1,
                "model_file_name": "workpiece_model.xml",
                "model_file": "<xml></xml>",
                "position_x": 1.504,
                "position_y": 3.574,
                "position_z": 4.154,
            }
        }


class WorkpieceCreate(WorkpieceBase):
    id: Optional[int]
    model_file: Optional[str]


class WorkpieceUpdate(WorkpieceBase):
    id: Optional[int]
    model_file: Optional[str]
    project_id: Optional[int]


# Properties shared by models stored in DB
class WorkpieceInDBBase(WorkpieceBase):
    model_file: Optional[str]

    class Config:
        orm_mode = True


class Workpiece(WorkpieceInDBBase):
    pass


class WorkpieceInDB(WorkpieceInDBBase):
    pass
