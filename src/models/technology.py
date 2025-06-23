from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.project_technology import project_technology


class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    icon = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"))

    projects = relationship(
        "Project",
        secondary=project_technology,
        back_populates="technologies",
    )
