import pytest
from typing import Generator, Callable
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database import Base
from src.main import app
from src.dependencies import get_db
from src.core.config import settings, SRC_DIR
from src.core.security import create_access_token, get_password_hash
from src.models.user import User
import os
import shutil
import io
from PIL import Image



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
    
    test_images_dir = SRC_DIR / "static" / "images"
    if test_images_dir.exists():
        shutil.rmtree(test_images_dir)
    test_images_dir.mkdir(parents=True, exist_ok=True)

    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

# --- Fixture para obtener un Token de Autenticación de Administrador ---
@pytest.fixture(scope="function")
def admin_user(db_session: Session) -> User:
    """Creates an admin user with a known password for testing."""
    test_admin = User(
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash("testpassword"), # Use a known, simple password for tests
        role="admin",
        is_active=True,
    )
    db_session.add(test_admin)
    db_session.commit()
    db_session.refresh(test_admin)
    return test_admin

@pytest.fixture(scope="function")
def admin_auth_headers(admin_user: User) -> dict[str, str]:
    """Returns authentication headers for an admin user."""
    token = create_access_token(data={"sub": admin_user.username, "role": admin_user.role})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture(scope="function")
def create_test_image() -> Callable:
    """Returns a function to create a dummy image file for uploads."""
    def _create_image(filename: str = "test.jpg"):
        file = io.BytesIO()
        image = Image.new('RGB', (100, 100), 'red')
        image.save(file, 'jpeg')
        file.seek(0)
        return (filename, file, 'image/jpeg')
    return _create_image