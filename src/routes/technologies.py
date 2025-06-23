from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import technology as technology_schema
from services import technologies_service
from dependencies import get_db, get_current_admin_user
from utils import save_image

router = APIRouter(prefix="/technologies", tags=["Technologies"])


@router.post(
    "/",
    response_model=technology_schema.Technology,
    dependencies=[Depends(get_current_admin_user)],
)
def create_technology(
    db: Session = Depends(get_db),
    name: str = Form(...),
    color: str = Form(...),
    icon_file: UploadFile = File(..., alias="icon"),  # <-- Aceptamos el archivo
):

    icon_url = save_image(icon_file)

    technology_data = technology_schema.TechnologyCreate(
        name=name, color=color, icon=icon_url
    )

    return technologies_service.create_technology(db=db, technology=technology_data)


@router.put(
    "/{technology_id}",
    response_model=technology_schema.Technology,
    dependencies=[Depends(get_current_admin_user)],
)
def update_technology(
    technology_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    color: Optional[str] = Form(None),
    icon_file: Optional[UploadFile] = File(
        None, alias="icon"
    ),  # <-- El archivo es opcional
):
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if color is not None:
        update_data["color"] = color

    if icon_file:
        icon_url = save_image(icon_file)
        update_data["icon"] = icon_url

    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    technology_update_schema = technology_schema.TechnologyUpdate(**update_data)

    db_technology = technologies_service.update_technology(
        db, technology_id=technology_id, technology_data=technology_update_schema
    )

    if db_technology is None:
        raise HTTPException(status_code=404, detail="Technology not found")

    return db_technology


@router.get("/", response_model=List[technology_schema.Technology])
def read_technologies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return technologies_service.get_technologies(db, skip=skip, limit=limit)


@router.get("/{technology_id}", response_model=technology_schema.Technology)
def read_technology(technology_id: int, db: Session = Depends(get_db)):
    db_technology = technologies_service.get_technology(db, technology_id=technology_id)
    if db_technology is None:
        raise HTTPException(status_code=404, detail="Technology not found")
    return db_technology


@router.delete(
    "/{technology_id}",
    response_model=technology_schema.Technology,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_technology(technology_id: int, db: Session = Depends(get_db)):
    db_technology = technologies_service.delete_technology(
        db=db, technology_id=technology_id
    )
    if db_technology is None:
        raise HTTPException(status_code=404, detail="Technology not found")
    return db_technology
