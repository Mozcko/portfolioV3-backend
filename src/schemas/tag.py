from pydantic import BaseModel, ConfigDict
from typing import Optional

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str] = None

class Tag(TagBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
