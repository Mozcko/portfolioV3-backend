from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TechnologyBase(BaseModel):
    name: str
    icon: str

class TechnologyCreate(TechnologyBase):
    pass

class Technology(TechnologyBase):
    id: int
    project_id: int
    
    model_config = ConfigDict(from_attributes=True)

class TechnologyUpdate(TechnologyBase):
    name: Optional[str] = None
    icon: Optional[str] = None