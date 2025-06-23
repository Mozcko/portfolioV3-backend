import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database import Base
from src.main import app
from src.dependencies import get_db
from src.core.config import settings
from src.core.security import create_access_token
from src.models.user import User
from src.core.security import get_password_hash
import os
import shutil

# --- Configuración de la Base de Datos de Prueba ---
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Base de datos en memoria

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
    # Sobrescribir la dependencia get_db para usar la sesión de prueba
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    
    # Limpiar la carpeta de imágenes de prueba antes de cada test
    test_images_path = "src/static/images"
    if os.path.exists(test_images_path):
        shutil.rmtree(test_images_path)
    os.makedirs(test_images_path)

    with TestClient(app) as c:
        yield c
    
    # Limpiar la sobreescritura de la dependencia
    app.dependency_overrides.clear()


# --- Fixture para obtener un Token de Autenticación de Administrador ---
@pytest.fixture(scope="function")
def admin_auth_token(db_session) -> str:
    # Crear un usuario administrador de prueba
    test_admin = User(
        username=settings.ADMIN_USERNAME,
        email=settings.ADMIN_EMAIL,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD)
    )
    db_session.add(test_admin)
    db_session.commit()

    # Generar un token para este usuario
    token = create_access_token(data={"sub": settings.ADMIN_USERNAME})
    return f"Bearer {token}"