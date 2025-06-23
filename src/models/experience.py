from sqlalchemy import Column, Integer, String, Text

from database import Base

class Experience(Base):
    __tablename__ = 'experiences'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    icon_bg = Column(String, nullable=False)
    date = Column(String, nullable=False)
    points = Column(Text, nullable=False) 