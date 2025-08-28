from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional

from src.models.technology import Technology
from src.schemas import technology as technology_schema

from src.utils import save_image, delete_image

def get_technology(db: Session, technology_id: int):
    return db.query(Technology).filter(Technology.id == technology_id).first()


def get_technologies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Technology).offset(skip).limit(limit).all()


def create_technology(
    db: Session, technology: technology_schema.TechnologyCreate, image_file: UploadFile
) -> Technology:
    """
    Crea una tecnología y devuelve el objeto de la BD.
    """

    image_route = save_image(image_file)

    # Crear el objeto del modelo con los datos y la ruta de la imagen
    db_technology = Technology(
        **technology.model_dump(),
        icon=image_route
    )

    # Guardar en la base de datos
    db.add(db_technology)
    db.commit()
    db.refresh(db_technology)
    return db_technology


def update_technology(
    db: Session,
    technology_id: int,
    technology_data: technology_schema.TechnologyUpdate,
    image_file: Optional[UploadFile] = None
) -> Optional[Technology]:
    """
    Actualiza una tecnología
    """
    db_technology = get_technology(db, technology_id)
    if not db_technology:
        return None

    # Actualizar los campos de la tecnología
    update_data = technology_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_technology, key, value)

    # Si se subió un archivo nuevo
    if image_file:
        # 1. Borrar la imagen antigua
        if db_technology.icon:
            delete_image(db_technology.icon)
        
        # 2. Guardar la imagen nueva y actualizar la ruta
        new_image_route = save_image(image_file)
        db_technology.icon = new_image_route

    db.commit()
    db.refresh(db_technology)
    return db_technology


def delete_technology(db: Session, technology_id: int) -> Optional[Technology]:
    """
    Elimina un proyecto y su imagen asociada.
    """
    db_technology = get_technology(db, technology_id)
    if not db_technology:
        return None
    
    if db_technology.icon:
        delete_image(db_technology.icon)

    # Borrar el registro de la base de datos
    db.delete(db_technology)
    db.commit()
    return db_technology
