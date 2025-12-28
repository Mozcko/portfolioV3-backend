from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from .technology import Technology
from .tag import Tag

class ProjectBase(BaseModel):
    title: str
    description_en: str
    description_es: str
    project_url: str
    repo_url: Optional[str] = None


class ProjectCreate(ProjectBase):
    technology_ids: Optional[List[int]] = []
    tag_ids: Optional[List[int]] = []


class Project(ProjectBase):
    id: int
    image_route: str
    technologies: List[Technology] = []
    tags: List[Tag] = []
    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description_en: Optional[str] = None
    description_es: Optional[str] = None
    project_url: Optional[str] = None
    repo_url: Optional[str] = None
    image_route: Optional[str] = None
    technology_ids: Optional[List[int]] = None
    tag_ids: Optional[List[int]] = None
