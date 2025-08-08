from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional

from models.certificate import Certificate
from schemas import certificate as certificate_schema
from utils import save_image, delete_image

def get_certificate(db: Session, certificate_id: int):
    return db.query(Certificate).filter(Certificate.id == certificate_id).first()

def get_certificates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Certificate).offset(skip).limit(limit).all()

def create_certificate(db: Session, certificate: certificate_schema.CertificateCreate, image_file: UploadFile) -> Certificate:
    """
    Crea un certificado, guarda su imagen y devuelve el objeto de la BD.
    """
    # 1. Guardar la imagen y obtener la ruta
    image_route = save_image(image_file)
    
    # 2. Crear el objeto del modelo con los datos y la ruta de la imagen
    db_certificate = Certificate(
        **certificate.model_dump(),
        image_route=image_route
    )
    
    # 3. Guardar en la base de datos
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def update_certificate(
    db: Session, 
    certificate_id: int, 
    certificate_data: certificate_schema.CertificateUpdate, 
    image_file: Optional[UploadFile] = None
) -> Optional[Certificate]:
    """
    Actualiza un certificado. Si se proporciona una nueva imagen,
    reemplaza la anterior.
    """
    db_certificate = get_certificate(db, certificate_id)
    if not db_certificate:
        return None

    # Actualizar los campos del certificado
    update_data = certificate_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_certificate, key, value)

    # Si se subió un archivo nuevo
    if image_file:
        # 1. Borrar la imagen antigua
        if db_certificate.image_route:
            delete_image(db_certificate.image_route)
        
        # 2. Guardar la imagen nueva y actualizar la ruta
        new_image_route = save_image(image_file)
        db_certificate.image_route = new_image_route

    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def delete_certificate(db: Session, certificate_id: int) -> Optional[Certificate]:
    """
    Elimina un certificado y su imagen asociada.
    """
    db_certificate = get_certificate(db, certificate_id)
    if not db_certificate:
        return None
        
    # 1. Borrar la imagen del servidor
    if db_certificate.image_route:
        delete_image(db_certificate.image_route)
        
    # 2. Borrar el registro de la base de datos
    db.delete(db_certificate)
    db.commit()
    return db_certificate