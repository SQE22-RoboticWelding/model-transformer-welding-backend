from typing import Optional
from pydantic import BaseModel

from app.schemas.robot_type import RobotTypeBase


class RobotBase(BaseModel):
    id: int
    robot_type_id: int
    name: str
    description: Optional[str]
    position_x: float
    position_y: float
    position_z: float
    position_norm_vector_x: float
    position_norm_vector_y: float
    position_norm_vector_z: float

    class Config:
        schema_extra = {
            "example": {
                "robot_type_id": 1,
                "name": "Scratchy",
                "description": "Robot with the scratch on arm",
                "position_x": 0.554,
                "position_y": 5.554,
                "position_z": 15.554,
                "position_norm_vector_x": 0,
                "position_norm_vector_y": 0,
                "position_norm_vector_z": 1,
            }
        }


class RobotCreate(RobotBase):
    id: Optional[int]


class RobotUpdate(RobotBase):
    id: Optional[int]
    robot_type_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
    position_x: Optional[float]
    position_y: Optional[float]
    position_z: Optional[float]
    position_norm_vector_x: Optional[float]
    position_norm_vector_y: Optional[float]
    position_norm_vector_z: Optional[float]


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
