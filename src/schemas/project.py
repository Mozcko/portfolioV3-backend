from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from tag import TagCreate, Tag
from technology import Technology


class ProjectBase(BaseModel):
    name: str
    link: Optional[str] = None
    source_code: Optional[str] = None
    interest: str


class ProjectCreate(ProjectBase):
    image_url: str
    tags: List[TagCreate] = []
    technology_ids: List[int] = []


class Project(ProjectBase):
    id: int
    image_url: str
    tags: List[Tag] = []
    technologies: List[Technology] = []

    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None
    image_url: Optional[str] = None
    link: Optional[str] = None
    source_code: Optional[str] = None
    interest: Optional[str] = None
    tags: Optional[List[TagCreate]] = None
    technology_ids: Optional[List[int]] = None
