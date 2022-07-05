from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class WeldingPoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"))
    robot_id = Column(Integer, ForeignKey("robot.id"))
    welding_order = Column(Integer, index=True)
    name = Column(String)
    description = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    roll = Column(Float)
    pitch = Column(Float)
    yaw = Column(Float)
    tolerance = Column(Float)
    project = relationship("Project", back_populates="welding_points", lazy='subquery')
    robot = relationship("Robot", lazy='subquery')
