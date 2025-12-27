import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.core.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    # Configuración para SQLite (Desarrollo)
    # Construimos la ruta absoluta al archivo .db
    db_path = os.path.join(os.path.dirname(__file__), '..', settings.DATABASE_NAME)
    db_path = os.path.normpath(db_path)
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL + db_path
    connect_args = {"check_same_thread": False}
else:
    # Configuración para PostgreSQL (Producción)
    # En Postgres la URL ya viene completa, no necesitamos concatenar rutas de archivo
    SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
    connect_args = {}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()