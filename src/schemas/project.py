from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class ProjectBase(BaseModel):
    title: str
    description: str


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    image_route: str
    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_route: Optional[str] = None
