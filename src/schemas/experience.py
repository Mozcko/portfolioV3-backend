from pydantic import BaseModel, ConfigDict
from typing import Optional

class ExperienceBase(BaseModel):
    title: str
    company_name: str
    icon: str
    icon_bg: str
    date: str
    points: str #TODO: revisar la parte de JSON

class ExperienceCreate(ExperienceBase):
    pass

class Experience(ExperienceBase):
    model_config = ConfigDict(from_attributes=True)

class ExperienceUpdate(ExperienceBase):
    title: Optional[str]
    company_name: Optional[str]
    icon: Optional[str]
    icon_bg: Optional[str]
    date: Optional[str]
    points: Optional[str]

    class Config:
        form_attributes = True