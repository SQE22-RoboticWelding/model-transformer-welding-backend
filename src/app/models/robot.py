from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Robot(Base):
    id = Column(Integer, primary_key=True, index=True)
    robot_type_id = Column(Integer, ForeignKey("robottype.id"))
    description = Column(String)
    robot_type = relationship("RobotType", lazy='subquery')
