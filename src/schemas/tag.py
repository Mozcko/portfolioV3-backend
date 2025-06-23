from pydantic import BaseModel, ConfigDict
from typing import Optional

class TagBase(BaseModel):
    name: str
    color: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)

class TagUpdate(TagBase):
    name: Optional[str] = None
    color: Optional[str] = None