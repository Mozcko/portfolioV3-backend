from pydantic import BaseModel, ConfigDict
from typing import Optional


class CertificateBase(BaseModel):
    title: str
    school: str
    link: Optional[str] = None


class CertificateCreate(CertificateBase):
    pass


# El schema de respuesta sí debe incluir el ID y la ruta de la imagen.
class Certificate(CertificateBase):
    id: int
    image_route: str
    model_config = ConfigDict(from_attributes=True)


class CertificateUpdate(BaseModel):
    title: Optional[str] = None
    school: Optional[str] = None
    link: Optional[str] = None
    image_route: Optional[str] = None
