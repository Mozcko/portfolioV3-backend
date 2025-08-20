from pydantic import BaseModel, ConfigDict
from typing import Optional


class JobBase(BaseModel):
    title: str
    start_date: str
    end_date: str
    current_job: bool


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    start_date: str
    end_date: str
    current_job: bool
    image_route: str
    model_config = ConfigDict(from_attributes=True)


class JobUpdate(BaseModel):
    title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current_job: Optional[bool] = None
    image_route: Optional[str] = None
