from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from typing import List

from database import Base

# Association table for many-to-many relationship between projects and technologies
project_technologies = Table(
    'project_technologies',
    Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id'), primary_key=True),
    Column('technology_id', Integer, ForeignKey('technologies.id'), primary_key=True)
)

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_route = Column(String, nullable=False)
    
    # Many-to-many relationship with technologies
    technologies = relationship(
        "Technology",
        secondary=project_technologies,
        back_populates="projects",
        lazy="selectin"
    )
    

