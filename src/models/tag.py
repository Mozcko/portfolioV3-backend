from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.database import Base

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    
    # Back-reference to projects
    projects = relationship(
        "Project",
        secondary="project_tags",
        back_populates="tags",
        lazy="selectin"
    )
