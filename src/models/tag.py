from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.project_tag import project_tag


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    color = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"))

    projects = relationship(
        "Project",
        secondary=project_tag,
        back_populates="tags",  
    )
