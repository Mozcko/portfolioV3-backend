from pydantic import BaseModel, ConfigDict
from typing import Optional


# Esquema para la creación de usuario (no se usará en un endpoint público)
class UserCreate(BaseModel):
    username: str
    password: str


# Esquema para leer datos de un usuario (nunca exponer la contraseña)
class User(BaseModel):
    id: int
    username: str
    is_active: bool
    role: str

    model_config = ConfigDict(from_attributes=True)


# Esquemas para el token de autenticación
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
