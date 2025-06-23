import os
import logging
import uuid

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.core.logging import setup_logging
from database import engine, Base

from src.core.config import settings

from src.routes import auth, i18n, certificates, experiences, projects, technologies
from src.utils import create_admin_user_on_startup
from src.database import SessionLocal

from fastapi import UploadFile
from PIL import Image


cwd = os.getcwd()
static_path = os.path.abspath(os.path.join(cwd, "static"))
setup_logging()
logger = logging.getLogger(__name__)

def save_image(file: UploadFile, base_path: str = "src/static/images") -> str:
    # 1. Definir la ruta y asegurarse de que el directorio exista
    upload_dir = os.path.join(os.getcwd(), base_path)
    os.makedirs(upload_dir, exist_ok=True)

    # 2. Validar que el archivo es una imagen usando Pillow
    try:
        img = Image.open(file.file)
        img.verify()  # Intenta verificar la integridad de la imagen
        # Volver al inicio del archivo después de verificar
        file.file.seek(0)
    except Exception as e:
        logger.error(f"Error al validar la imagen: {e}")
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es una imagen válida.")

    # 3. Generar un nombre de archivo único para evitar colisiones
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)

    # 4. Guardar el archivo en el disco
    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
    except Exception as e:
        logger.error(f"No se pudo guardar el archivo: {e}")
        raise HTTPException(status_code=500, detail="No se pudo guardar el archivo de imagen.")

    # 5. Devolver la ruta pública
    public_url_path = f"/static/images/{unique_filename}"
    logger.info(f"Imagen '{unique_filename}' guardada exitosamente en '{public_url_path}'")
    
    return public_url_path


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación y creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    create_admin_user_on_startup()
    yield
    logger.info("Apagando aplicación...")


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=settings.ALLOWED_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
    expose_headers=settings.ALLOWED_EXPOSED_HEADERS,
)

# ruta para archivos estáticos
app.mount("/static", StaticFiles(directory="src/static"), name="static")

# rutas de la aplicación
app.include_router(auth.router)
app.include_router(i18n.router)
app.include_router(certificates.router)
app.include_router(experiences.router)
app.include_router(projects.router)
app.include_router(technologies.router)
