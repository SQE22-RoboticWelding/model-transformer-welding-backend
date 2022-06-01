from typing import Optional
from pydantic import BaseModel


class RobotBase(BaseModel):
    description: Optional[str] = None
    robot_type_id: int

    class Config:
        schema_extra = {
            "example": {
                "robot_type_id": 1,
                "description": "Robot with the scratch on arm"
            }
        }


class RobotCreate(RobotBase):
    pass

class RobotUpdate(RobotBase):
    robot_type_id: Optional[int]


# Properties shared by models stored in DB
class RobotInDBBase(RobotBase):
    id: int

    class Config:
        orm_mode = True


class Robot(RobotInDBBase):
    pass


class RobotInDB(RobotInDBBase):
    pass
