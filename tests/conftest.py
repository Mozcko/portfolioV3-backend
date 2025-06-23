import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from main import app
from dependencies import get_db
from core.config import settings
from core.security import create_access_token, get_password_hash
from models.user import User
import os
import shutil


# --- Configuración de la Base de Datos de Prueba ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Creación y Eliminación de Tablas ---
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# --- Fixture para la Sesión de la Base de Datos ---
@pytest.fixture(scope="function")
def db_session() -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

# --- Fixture para el Cliente de Prueba de FastAPI ---
@pytest.fixture(scope="function")
def client(db_session: Generator) -> Generator:
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    test_images_path = "src/static/images"
    if os.path.exists(test_images_path):
        shutil.rmtree(test_images_path)
    os.makedirs(test_images_path)

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()


# --- Fixture para obtener un Token de Autenticación de Administrador ---
@pytest.fixture(scope="function")
def admin_auth_token(db_session) -> str:
    test_admin = User(
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD)
    )
    db_session.add(test_admin)
    db_session.commit()

    token = create_access_token(data={"sub": settings.ADMIN_USERNAME})
    return f"Bearer {token}"