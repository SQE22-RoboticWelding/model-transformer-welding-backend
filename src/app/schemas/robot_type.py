from typing import Optional
from pydantic import BaseModel


class RobotTypeBase(BaseModel):
    id: int
    name: str
    vendor: str
    capacity_load_kg: Optional[float]
    range_m: Optional[float]

    class Config:
        schema_extra = {
            "example": {
                "name": "Niryo One",
                "vendor": "Niryo",
                "capacity_load_kg": 50.5,
                "range_m": 3.141
            }
        }


class RobotTypeCreate(RobotTypeBase):
    id: Optional[int]


class RobotTypeUpdate(RobotTypeBase):
    id: Optional[int]
    name: Optional[str]
    vendor: Optional[str]


# Properties shared by models stored in DB
class RobotTypeInDBBase(RobotTypeBase):
    class Config:
        orm_mode = True


class RobotType(RobotTypeInDBBase):
    pass


class RobotTypeInDB(RobotTypeInDBBase):
    pass
