import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .core.config import settings

# Usamos una ruta relativa a la carpeta 'src'
db_path = os.path.join(os.path.dirname(__file__), '..', settings.DATABASE_NAME)
db_path = os.path.normpath(db_path)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL + db_path

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # Necesario solo para SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()