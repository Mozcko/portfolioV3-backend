from sqlalchemy import Column, Integer, String

from src.database import Base


class Social(Base):
    __tablename__ = "socials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    link = Column(String, nullable=False)
    image_route = Column(String, nullable=False)