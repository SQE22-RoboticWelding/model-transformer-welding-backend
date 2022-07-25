from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Workpiece(Base):
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False)
    model_file_name = Column(String)
    model_file = Column(String)
    position_x = Column(Float)
    position_y = Column(Float)
    position_z = Column(Float)
    project = relationship("Project", back_populates="workpiece", lazy="subquery")
