from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from ..database import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    school = Column(String(255), nullable=False)
    link = Column(String(500), nullable=True)
    image_route = Column(String(500), nullable=False)
