from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from .project_technology import project_technologies
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description_en = Column(String, nullable=False)
    description_es = Column(String, nullable=False)
    image_route = Column(String, nullable=False)
    
    # Many-to-many relationship with technologies
    technologies = relationship(
        "Technology",
        secondary=project_technologies,
        back_populates="projects",
        lazy="selectin"
    )
    

