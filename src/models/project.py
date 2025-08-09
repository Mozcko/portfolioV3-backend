from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from typing import List

from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    image_route = Column(String, nullable=False)
    

