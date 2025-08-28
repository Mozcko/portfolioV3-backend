from pydantic import BaseModel, ConfigDict
from typing import Optional


class SocialBase(BaseModel):
    name: str
    link: str


class SocialCreate(SocialBase):
    pass


class SocialUpdate(BaseModel):
    name: Optional[str] = None
    link: Optional[str] = None


class Social(SocialBase):
    id: int
    image_route: str
    model_config = ConfigDict(from_attributes=True)