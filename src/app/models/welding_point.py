from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class WeldingPoint(Base):
    id = Column(Integer, primary_key=True, index=True)
    welding_configuration_id = Column(Integer, ForeignKey("weldingconfiguration.id"))
    robot_id = Column(Integer, ForeignKey("robot.id"))
    welding_order = Column(Integer, index=True)
    description = Column(String)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)
    roll = Column(Float)
    pitch = Column(Float)
    yaw = Column(Float)
    tolerance = Column(Float)
    welding_configuration = relationship("WeldingConfiguration", back_populates="welding_points", lazy='subquery')
