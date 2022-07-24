from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Robot(Base):
    id = Column(Integer, primary_key=True, index=True)
    robot_type_id = Column(Integer, ForeignKey("robottype.id"))
    project_id = Column(Integer, ForeignKey("project.id"))
    name = Column(String)
    description = Column(String)
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float)
    robot_type = relationship("RobotType", back_populates="robots", lazy="subquery")
    project = relationship("Project", back_populates="robots", lazy="subquery")
