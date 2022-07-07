from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class WeldingPoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    robot_id = Column(Integer, ForeignKey("robot.id"))
    welding_order = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    x = Column(Float, nullable=False)
    y = Column(Float, nullable=False)
    z = Column(Float, nullable=False)
    x_original = Column(Float, nullable=False)
    y_original = Column(Float, nullable=False)
    z_original = Column(Float, nullable=False)
    roll = Column(Float, nullable=False)
    pitch = Column(Float, nullable=False)
    yaw = Column(Float, nullable=False)
    tolerance = Column(Float)
    project = relationship("Project", back_populates="welding_points", lazy='subquery')
    robot = relationship("Robot", lazy='subquery')
