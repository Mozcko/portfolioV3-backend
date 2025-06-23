from pydantic import BaseModel, ConfigDict
from typing import Optional

class CertificateBase(BaseModel):
    title: str
    school: str
    link: Optional[str] = None

class CertificateCreate(CertificateBase):
    image_route: str
    

class Certificate(CertificateBase):
    image_route: str
    model_config = ConfigDict(from_attributes=True)

class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    school: Optional[str] = None
    link: Optional[str] = None
    image_route: Optional[str] = None

    class Config:
        form_attributes = True
