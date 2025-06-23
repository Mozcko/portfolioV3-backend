from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TechnologyBase(BaseModel):
    name: str
    

class TechnologyCreate(TechnologyBase):
    icon: str

class Technology(TechnologyBase):
    id: int
    icon: str
    project_id: int
    
    model_config = ConfigDict(from_attributes=True)

class TechnologyUpdate(TechnologyBase):
    name: Optional[str] = None
    color: Optional[str] = None
    icon: Optional[str] = None

    class Config:
        from_attributes = True