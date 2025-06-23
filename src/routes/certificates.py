from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import certificate as certificate_schema
from services import certificates_service
from dependencies import get_db, get_current_admin_user
from utils import save_image

router = APIRouter(prefix="/certificates", tags=["Certificates"])

@router.post("/", response_model=certificate_schema.Certificate, dependencies=[Depends(get_current_admin_user)])
def create_certificate(
    db: Session = Depends(get_db),
    title: str = Form(...),
    school: str = Form(...),
    link: Optional[str] = Form(None),
    file: UploadFile = File(...)  # <-- Acepta el archivo aquí
):

    image_url = save_image(file)

    certificate_data = certificate_schema.CertificateCreate(
        title=title,
        school=school,
        link=link,
        image_route=image_url  
    )

    return certificates_service.create_certificate(db=db, certificate=certificate_data)

@router.get("/", response_model=List[certificate_schema.Certificate])
def read_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    certificates = certificates_service.get_certificates(db, skip=skip, limit=limit)
    return certificates

@router.get("/{certificate_id}", response_model=certificate_schema.Certificate)
def read_certificate(certificate_id: int, db: Session = Depends(get_db)):
    db_certificate = certificates_service.get_certificate(db, certificate_id=certificate_id)
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return db_certificate

@router.put("/{certificate_id}", response_model=certificate_schema.Certificate, dependencies=[Depends(get_current_admin_user)])
def update_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    school: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None) # <-- El archivo es opcional en la actualización
):

    db_certificate = certificates_service.get_certificate(db, certificate_id=certificate_id)
    if not db_certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")

    update_data = {}
    if title is not None:
        update_data['title'] = title
    if school is not None:
        update_data['school'] = school
    if link is not None:
        update_data['link'] = link

    
    if file:
        image_url = save_image(file)
        update_data['image_route'] = image_url
        # TODO: borrar la imagen antigua del servidor

    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    certificate_schema_update = certificate_schema.CertificateUpdate(**update_data)
    
    return certificates_service.update_certificate(
        db, certificate_id=certificate_id, certificate_data=certificate_schema_update
    )

@router.delete("/{certificate_id}", response_model=certificate_schema.Certificate, dependencies=[Depends(get_current_admin_user)])
def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    # TODO: borrar la imagen del servidor
    db_certificate = certificates_service.delete_certificate(db=db, certificate_id=certificate_id)
    if db_certificate is None:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return db_certificate