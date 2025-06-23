from sqlalchemy.orm import Session
from models.certificate import Certificate
from schemas import certificate as certificate_schema

def get_certificate(db: Session, certificate_id: int):
    return db.query(Certificate).filter(Certificate.id == certificate_id).first()

def get_certificates(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Certificate).offset(skip).limit(limit).all()

def create_certificate(db: Session, certificate: certificate_schema.CertificateCreate):
    db_certificate = Certificate(**certificate.model_dump())
    db.add(db_certificate)
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def update_certificate(db: Session, certificate_id: int, certificate_data: certificate_schema.CertificateUpdate):
    db_certificate = get_certificate(db, certificate_id)
    if not db_certificate:
        return None
    
    update_data = certificate_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_certificate, key, value)
        
    db.commit()
    db.refresh(db_certificate)
    return db_certificate

def delete_certificate(db: Session, certificate_id: int):
    db_certificate = get_certificate(db, certificate_id)
    if not db_certificate:
        return None
    db.delete(db_certificate)
    db.commit()
    return db_certificate