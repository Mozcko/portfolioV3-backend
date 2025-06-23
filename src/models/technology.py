from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    icon = Column(String(255), nullable=False) 
    
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="technologies")
