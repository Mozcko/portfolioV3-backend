from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import technology as technology_schema
from services import technology_service
from dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/technologies", tags=["Technologies"])


@router.post(
    "/",
    response_model=technology_schema.Technology,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
    summary="Create a new technology",
    description="Creates a new technology with a name and an icon image. Requires admin authentication.",
)
def create_technology(
    name: str = Form(...),
    icon: UploadFile = File(...),  # <-- ¡CORRECCIÓN AQUÍ! Se cambió Form por File
    db: Session = Depends(get_db),
):
    technology_create = technology_schema.TechnologyCreate(name=name)

    return technology_service.create_technology(
        db=db, technology=technology_create, image_file=icon # Ahora 'icon' es el archivo subido
    )


@router.get("/", response_model=List[technology_schema.Technology], summary="Get all technologies")
def read_technologies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieves a list of all available technologies.
    """
    return technology_service.get_technologies(db=db, skip=skip, limit=limit)


@router.get("/{technology_id}", response_model=technology_schema.Technology, summary="Get a single technology by ID")
def read_technology(technology_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the details of a specific technology by its ID.
    """
    db_technology = technology_service.get_technology(db=db, technology_id=technology_id)
    if db_technology is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_technology


@router.put(
    "/{technology_id}",
    response_model=technology_schema.Technology,
    dependencies=[Depends(get_current_admin_user)],
    summary="Update a technology",
    description="Updates a technology's name and/or icon. Requires admin authentication.",
)
def update_technology(
    technology_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None),  # CORRECCIÓN 1: Usar File en lugar de Form
):
    # CORRECCIÓN 2: El objeto de actualización solo debe llevar los datos del formulario, no el archivo.
    update_data = technology_schema.TechnologyUpdate(name=name)

    # CORRECCIÓN 3: Validar que se envíe al menos un dato para actualizar.
    if name is None and image_file is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay datos para actualizar",
        )

    # CORRECCIÓN 4: Usar los nombres de argumento correctos ('technology_data' y 'image_file').
    updated_technology = technology_service.update_technology(
        db=db,
        technology_id=technology_id,
        technology_data=update_data,
        image_file=image_file,
    )

    if updated_technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Technology not found"
        )

    return updated_technology


@router.delete(
    "/{technology_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
    summary="Delete a technology",
    description="Deletes a technology and its associated icon image from the server. Requires admin authentication.",
)
def delete_technology(technology_id: int, db: Session = Depends(get_db)):
    """
    Deletes a technology by its ID.
    """
    db_technology = technology_service.delete_technology(
        db=db, technology_id=technology_id
    )
    if db_technology is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )
    return None
