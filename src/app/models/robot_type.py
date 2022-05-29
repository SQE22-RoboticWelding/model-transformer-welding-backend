from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base
from sqlalchemy.orm import relationship


class RobotType(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    vendor = Column(String)
    capacity_load_kg = Column(Float)
    range_m = Column(Float)
    robots = relationship("Robot", back_populates="robot_type", lazy='joined')
