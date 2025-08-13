from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class TechnologyBase(BaseModel):
    name: str


class TechnologyCreate(TechnologyBase):
    pass


class Technology(TechnologyBase):
    id: int
    icon: str
    model_config = ConfigDict(from_attributes=True)


class TechnologyUpdate(BaseModel):
    name: Optional[str] = None
    icon: Optional[str] = None
