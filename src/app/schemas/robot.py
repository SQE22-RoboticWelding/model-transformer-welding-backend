from typing import Optional
from pydantic import BaseModel

from app.schemas.robot_type import RobotTypeBase


class RobotBase(BaseModel):
    id: int
    description: Optional[str]
    robot_type_id: int

    class Config:
        schema_extra = {
            "example": {
                "robot_type_id": 1,
                "description": "Robot with the scratch on arm"
            }
        }


class RobotCreate(RobotBase):
    id: Optional[int]


class RobotUpdate(RobotBase):
    id: Optional[int]
    robot_type_id: Optional[int]


class RobotWithType(RobotBase):
    robot_type: RobotTypeBase

    @staticmethod
    def factory(robot: RobotBase, robot_type: RobotTypeBase):
        dict_obj = robot.as_dict()
        dict_obj["robot_type"] = robot_type.as_dict()
        return RobotWithType(**dict_obj)


# Properties shared by models stored in DB
class RobotInDBBase(RobotBase):
    class Config:
        orm_mode = True


class Robot(RobotInDBBase):
    pass


class RobotInDB(RobotInDBBase):
    pass
