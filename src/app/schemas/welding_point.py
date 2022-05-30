from typing import Optional
from pydantic import BaseModel


class WeldingPointBase(BaseModel):
    robot_id: Optional[int] = None
    welding_configuration_id: int
    description: Optional[str] = None
    welding_order: int
    name: Optional[str] = None
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    tolerance: float

    class Config:
        schema_extra = {
            "example": {
                "welding_configuration_id": 1,
                "robot_id": 1,
                "welding_order": 1,
                "name": "Reactor vulnerability entrance",
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
    robot_type_id: int
    welding_configuration_id: int
    description: str
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    tolerance: float


class WeldingPointUpdate(WeldingPointBase):
    robot_id: int
    description: str
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    tolerance: float


# Properties shared by models stored in DB
class WeldingPointInDBBase(WeldingPointBase):
    id: int
    welding_configuration_id: int
    description: str
    robot_id: int
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    tolerance: float

    class Config:
        orm_mode = True


class WeldingPoint(WeldingPointInDBBase):
    pass


class WeldingPointInDB(WeldingPointInDBBase):
    pass
