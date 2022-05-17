from pydantic import BaseModel


class RobotTypeBase(BaseModel):
    name: str
    vendor: str


class RobotTypeCreate(RobotTypeBase):
    name: str
    vendor: str


class RobotTypeUpdate(RobotTypeBase):
    name: str
    vendor: str