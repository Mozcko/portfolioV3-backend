from pydantic import BaseModel, ConfigDict
from typing import Optional

class ExperienceBase(BaseModel):
    title: str
    company_name: str
    icon_bg: str
    date: str
    points: str 

class ExperienceCreate(ExperienceBase):
    icon: str

class Experience(ExperienceBase):
    icon: str
    model_config = ConfigDict(from_attributes=True)

class ExperienceUpdate(ExperienceBase):
    title: Optional[str] = None
    company_name: Optional[str] = None
    icon: Optional[str] = None
    icon_bg: Optional[str] = None
    date: Optional[str] = None
    points: Optional[str] = None

    class Config:
        form_attributes = True