from typing import Optional
from pydantic import BaseModel


class WeldingPointBase(BaseModel):
    id: int
    welding_configuration_id: int
    robot_id: Optional[int] = None
    welding_order: int
    description: Optional[str] = None
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
                "welding_configuration_id": 1,
                "robot_id": 1,
                "welding_order": 1,
                "description": "Reactor vulnerability entrance",
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
    welding_configuration_id: Optional[int]
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
