from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import project as project_schema
from services import projects_service
from dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/projects", tags=["Projects"])


# TODO: add documentation on the API
@router.post(
    "/",
    response_model=project_schema.Project,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_project(
    title: str = Form(...),
    description: Optional[str] = Form(...),
    image: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    project_create = project_schema.ProjectCreate(title=title, description=description)

    return projects_service.create_project(
        db=db, project=project_create, image_file=image
    )


# TODO: add documentation on the API
@router.get("/", response_model=List[project_schema.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return projects_service.get_projects(db=db, skip=skip, limit=limit)


# TODO: add documentation on the API
@router.get("/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):

    db_project = projects_service.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_project


# TODO: add documentation on the API
@router.put(
    "/{project_id}",
    response_model=project_schema.Project,
    dependencies=[Depends(get_current_admin_user)],
)
def update_project(
    project_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
):
    update_data = project_schema.ProjectUpdate(title=title, description=description)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay datos para actualizar",
        )

    updated_project = projects_service.update_project(
        db=db, project_id=project_id, project_data=update_data, image_file=image
    )

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return updated_project


# TODO: add documentation on the API
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_service.delete_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Certificate not found"
        )
    
    return None
