from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # --- Configuración de la App ---
    APP_TITLE: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    
    # --- Configuración de la Base de Datos ---
    DATABASE_URL: str
    DATABASE_NAME: str

    # --- Configuración de Seguridad ---
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # --- Configuración de CORS ---
    ALLOWED_HOSTS: List[str] = []
    ALLOWED_METHODS: List[str] = ["*"]
    ALLOWED_HEADERS: List[str] = ["*"]
    ALLOWED_EXPOSED_HEADERS: List[str] = []
    ALLOWED_CREDENTIALS: bool = False

    class Config:
        env_file = ".env"
        extra = 'ignore'

settings = Settings()