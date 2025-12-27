# src/models/media.py
from sqlalchemy import Column, Integer, String, LargeBinary
from src.database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    content_type = Column(String)
    data = Column(LargeBinary)
