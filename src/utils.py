import os
import logging
import uuid

from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models.user import User
from src.models.media import Media
from src.core.config import settings, SRC_DIR
from src.core.security import get_password_hash
from fastapi import UploadFile, HTTPException
from PIL import Image

logger = logging.getLogger(__name__)


def create_admin_user_on_startup():
    """
    Crea un usuario administrador al iniciar la aplicación si no existe.
    Esta función se llama desde el evento 'lifespan' en main.py.
    """
    # Se crea una nueva sesión de DB exclusivamente para esta operación
    db: Session = SessionLocal()

    try:
        # Busca si el usuario administrador ya existe
        admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()

        if not admin:
            # Si no existe, crea el hash de la contraseña
            hashed_password = get_password_hash(settings.ADMIN_PASSWORD)

            # Crea la nueva instancia del usuario administrador
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                hashed_password=hashed_password,
                role="admin",
            )

            # Añade, confirma y refresca el nuevo usuario en la DB
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info("Usuario administrador creado exitosamente.")
        else:
            logger.info(
                "El usuario administrador ya existe. No se realizaron acciones."
            )

    finally:
        # Asegura que la sesión de la base de datos se cierre siempre
        db.close()


def save_image(db: Session, file: UploadFile) -> str:

    # 2. Validar que el archivo es una imagen usando Pillow
    try:
        img = Image.open(file.file)
        img.verify()  # Intenta verificar la integridad de la imagen
        # Volver al inicio del archivo después de verificar
        file.file.seek(0)
    except Exception as e:
        logger.error(f"Error al validar la imagen: {e}")
        raise HTTPException(
            status_code=400, detail="El archivo proporcionado no es una imagen válida."
        )

    # 3. Generar un nombre de archivo único para evitar colisiones
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"

    # 4. Guardar el archivo en la Base de Datos
    try:
        new_image = Media(
            filename=unique_filename,
            content_type=file.content_type,
            data=file.file.read()
        )
        db.add(new_image)
        db.commit()
        db.refresh(new_image)
    except Exception as e:
        logger.error(f"No se pudo guardar la imagen en la BD: {e}")
        raise HTTPException(
            status_code=500, detail="No se pudo guardar la imagen."
        )

    # 5. Devolver la ruta pública
    public_url_path = f"/static/images/{unique_filename}"
    logger.info(
        f"Imagen '{unique_filename}' guardada exitosamente en '{public_url_path}'"
    )

    return public_url_path


def delete_image(db: Session, image_route: str) -> None:
    """
    Elimina una imagen de la base de datos.
    """
    if not image_route.startswith("/static/images/"):
        logger.warning(
            f"La ruta de la imagen no tiene el formato esperado: {image_route}"
        )
        return

    filename = image_route.split("/")[-1]
    
    media = db.query(Media).filter(Media.filename == filename).first()
    
    if media:
        db.delete(media)
        db.commit()
        logger.info(f"Imagen '{filename}' eliminada de la BD exitosamente.")
    else:
        logger.warning(f"Se intentó eliminar una imagen que no existe en BD: {filename}")
