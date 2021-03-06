from typing import Optional
from pydantic import BaseModel


class WeldingPointBase(BaseModel):
    id: int
    project_id: int
    robot_id: Optional[int]
    welding_order: int
    name: Optional[str]
    description: Optional[str]
    x_original: float
    y_original: float
    z_original: float
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    tolerance: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "project_id": 1,
                "robot_id": 1,
                "welding_order": 1,
                "name": "P1",
                "description": "Reactor vulnerability entrance",
                "x_original": 9,
                "y_original": 16,
                "z_original": 12.25,
                "x": 10,
                "y": 15,
                "z": 12.5,
                "roll": 6.6,
                "pitch": 6.7,
                "yaw": 3,
                "tolerance": 0
            }
        }


class WeldingPointCreate(WeldingPointBase):
    id: Optional[int]
    pass


class WeldingPointUpdate(WeldingPointBase):
    id: Optional[int]
    project_id: Optional[int]
    x_original: Optional[float]
    y_original: Optional[float]
    z_original: Optional[float]
    x: Optional[float]
    y: Optional[float]
    z: Optional[float]
    roll: Optional[float]
    pitch: Optional[float]
    yaw: Optional[float]
    welding_order: Optional[int]


# Properties shared by models stored in DB
class WeldingPointInDBBase(WeldingPointBase):
    class Config:
        orm_mode = True


class WeldingPoint(WeldingPointInDBBase):
    pass


class WeldingPointInDB(WeldingPointInDBBase):
    pass
