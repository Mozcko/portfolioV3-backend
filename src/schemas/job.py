from pydantic import BaseModel, ConfigDict
from typing import Optional


class JobBase(BaseModel):
    title: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    image_route: str
    model_config = ConfigDict(from_attributes=True)


class JobUpdate(BaseModel):
    title: Optional[str] = None
    image_route: Optional[str] = None
