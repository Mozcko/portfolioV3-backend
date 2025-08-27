from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import certificate as certificate_schema
from services import certificates_service
from dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/certificates", tags=["Certificates"])


@router.post(
    "/",
    response_model=certificate_schema.Certificate,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_certificate(
    title: str = Form(...),
    school: str = Form(...),
    link: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Crea un nuevo certificado con su imagen.
    """
    certificate_create = certificate_schema.CertificateCreate(
        title=title, school=school, link=link
    )

    return certificates_service.create_certificate(
        db=db, certificate=certificate_create, image_file=file
    )


@router.get("/", response_model=List[certificate_schema.Certificate])
def read_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los certificados.
    """
    return certificates_service.get_certificates(db, skip=skip, limit=limit)


@router.get("/{certificate_id}", response_model=certificate_schema.Certificate)
def read_certificate(certificate_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un certificado por su ID.
    """
    db_certificate = certificates_service.get_certificate(
        db, certificate_id=certificate_id
    )
    if db_certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )
    return db_certificate


@router.put(
    "/{certificate_id}",
    response_model=certificate_schema.Certificate,
    dependencies=[Depends(get_current_admin_user)],
)
def update_certificate(
    certificate_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    school: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Actualiza un certificado. Permite cambiar datos y/o la imagen.
    """
    update_data = certificate_schema.CertificateUpdate(
        title=title, school=school, link=link
    )

    # Valida que al menos un campo se esté actualizando
    if not update_data.model_dump(exclude_unset=True) and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay datos para actualizar",
        )

    updated_certificate = certificates_service.update_certificate(
        db=db,
        certificate_id=certificate_id,
        certificate_data=update_data,
        image_file=file,
    )

    if updated_certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )

    return updated_certificate


@router.delete(
    "/{certificate_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_certificate(certificate_id: int, db: Session = Depends(get_db)):
    """
    Elimina un certificado y su imagen asociada.
    """
    db_certificate = certificates_service.delete_certificate(
        db=db, certificate_id=certificate_id
    )
    if db_certificate is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )

    # Devuelve una respuesta 204 sin contenido como es estándar para DELETE
    return None
