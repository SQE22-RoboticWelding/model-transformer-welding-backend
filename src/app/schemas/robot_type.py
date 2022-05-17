from typing import Optional
from pydantic import BaseModel


class RobotTypeBase(BaseModel):
    name: str = None
    vendor: Optional[str] = None


class RobotTypeCreate(RobotTypeBase):
    name: str
    vendor: str


class RobotTypeUpdate(RobotTypeBase):
    name: str
    vendor: str


# Properties shared by models stored in DB
class RobotTypeInDBBase(RobotTypeBase):
    id: int
    name: str
    vendor: str

    class Config:
        orm_mode = True


class RobotType(RobotTypeInDBBase):
    pass


class RobotTypeInDB(RobotTypeInDBBase):
    pass
