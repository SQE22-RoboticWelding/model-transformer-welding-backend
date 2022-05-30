from typing import Optional
from pydantic import BaseModel


class RobotTypeBase(BaseModel):
    name: str = None
    vendor: Optional[str] = None
    capacity_load_kg: Optional[float] = None
    range_m: Optional[float] = None

    class Config:
        schema_extra = {
            "example": {
                "robot_type_id": 1,
                "name": "Niryo One",
                "vendor": "Niryo",
                "capacity_load_kg": 50,
                "range_m": 3
            }
        }


class RobotTypeCreate(RobotTypeBase):
    name: str
    vendor: str
    capacity_load_kg: float
    range_m: float


class RobotTypeUpdate(RobotTypeBase):
    name: str
    vendor: str
    capacity_load_kg: float
    range_m: float


# Properties shared by models stored in DB
class RobotTypeInDBBase(RobotTypeBase):
    id: int
    name: str
    vendor: str
    capacity_load_kg: float
    range_m: float

    class Config:
        orm_mode = True


class RobotType(RobotTypeInDBBase):
    pass


class RobotTypeInDB(RobotTypeInDBBase):
    pass
