from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.project_technology import project_technology
from models.project_tag import project_tag


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    image_url = Column(String)
    project_url = Column(String)
    
    tags = relationship(
        "Tag",
        secondary=project_tag,
        back_populates="projects",  
    )

    technologies = relationship(
        "Technology",
        secondary=project_technology,
        back_populates="projects",  
    )
