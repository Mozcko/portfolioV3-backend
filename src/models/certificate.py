from sqlalchemy import Column, Integer, String

from database import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    school = Column(String, nullable=False)
    image_route = Column(String, nullable=False)
    link = Column(String, nullable=True)

