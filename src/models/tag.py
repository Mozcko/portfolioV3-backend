from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    color = Column(String, nullable=False)

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="tags")
