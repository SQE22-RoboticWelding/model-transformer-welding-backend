from sqlalchemy import Column, Integer, String, DateTime, FLOAT
from sqlalchemy.sql import func
from app.db.base_class import Base


class GenerationTemplate(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    language = Column(String)
    file_extension = Column(String)
    version = Column(FLOAT(precision=2), nullable=False)
    content = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    modified_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
