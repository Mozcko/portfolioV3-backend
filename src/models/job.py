from sqlalchemy import Column, Integer, String, Boolean

from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=True)
    current_job = Column(Boolean, nullable=False)
    image_route = Column(String, nullable=False)

    