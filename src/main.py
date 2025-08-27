import os
import logging

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from core.logging import setup_logging
from database import engine, Base
from core.config import settings, SRC_DIR
from routes import auth, i18n, certificates, projects, technologies, jobs, cv
from utils import create_admin_user_on_startup
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación y creando tablas de la base de datos...")
    # Asegurarse de que el directorio estático exista
    (SRC_DIR / "static").mkdir(exist_ok=True)
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
app.mount("/static", StaticFiles(directory=(SRC_DIR / "static")), name="static")

# rutas de la aplicación
app.include_router(auth.router, prefix="/auth")
app.include_router(i18n.router)
app.include_router(certificates.router)
app.include_router(projects.router)
app.include_router(technologies.router)
app.include_router(jobs.router)
app.include_router(cv.router)
