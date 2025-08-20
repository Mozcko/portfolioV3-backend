from pydantic import BaseModel, ConfigDict
from typing import Optional, List

from schemas.technology import Technology

class ProjectBase(BaseModel):
    title: str
    description_en: str
    description_es: str


class ProjectCreate(ProjectBase):
    technology_ids: Optional[List[int]] = []


class Project(ProjectBase):
    id: int
    image_route: str
    technologies: List[Technology] = []
    model_config = ConfigDict(from_attributes=True)


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description_en: Optional[str] = None
    description_es: Optional[str] = None
    image_route: Optional[str] = None
    technology_ids: Optional[List[int]] = None
