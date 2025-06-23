from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    link = Column(String, nullable=True)
    source_code = Column(String, nullable=True)
    interest = Column(String, nullable=False)

    tags = relationship(
        "tag", back_populates="project", cascade="all, delete-orphan"
    )

    technologies = relationship(
        "technology", back_populates="project", cascade="all, delete-orphan"
    )