import logging  
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from core.config import settings
from core.security import get_password_hash

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
                role="admin"
            )
            
            # Añade, confirma y refresca el nuevo usuario en la DB
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            logger.info("Usuario administrador creado exitosamente.")
        else:
            logger.info("El usuario administrador ya existe. No se realizaron acciones.")
            
    finally:
        # Asegura que la sesión de la base de datos se cierre siempre
        db.close()