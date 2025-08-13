from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    icon = Column(String, nullable=False)
    
    # Back-reference to projects
    projects = relationship(
        "Project",
        secondary="project_technologies",
        back_populates="technologies",
        lazy="selectin"
    )
    
    
