from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Form,
    File,
    UploadFile,
    status,
    Request,
)
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas import project as project_schema
from ..services import projects_service
from ..dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post(
    "/",
    response_model=project_schema.Project,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_project(
    title: str = Form(...),
    description_en: str = Form(...),
    description_es: str = Form(...),
    image: UploadFile = File(...),
    technology_ids: Optional[str] = Form(...),
    db: Session = Depends(get_db),
):
    """Create a new project with associated technologies."""

    # Parse technology IDs from string
    tech_ids = []
    if technology_ids:
        try:
            tech_ids = [
                int(id.strip()) for id in technology_ids.split(",") if id.strip()
            ]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid technology IDs format",
            )

    project_create = project_schema.ProjectCreate(
        title=title,
        description_en=description_en,
        description_es=description_es,
        technology_ids=tech_ids,
    )

    return projects_service.create_project(
        db=db, project=project_create, image_file=image
    )


@router.get("/", response_model=List[project_schema.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects with their technologies."""
    return projects_service.get_projects(db=db, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    """Get a single project with its technologies."""
    db_project = projects_service.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_project


@router.put(
    "/{project_id}",
    response_model=project_schema.Project,
    dependencies=[Depends(get_current_admin_user)],
)
def update_project(
    project_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    description_en: Optional[str] = Form(None),
    description_es: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    technology_ids: Optional[str] = Form(None),
):
    """Update a project including its technology associations."""

    # Parse technology IDs from string
    tech_ids = None
    if technology_ids is not None:
        try:
            tech_ids = [
                int(id.strip()) for id in technology_ids.split(",") if id.strip()
            ]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid technology IDs format",
            )

    update_data = project_schema.ProjectUpdate(
        title=title,
        description_en=description_en,
        description_es=description_es,
        technology_ids=tech_ids,
    )

    updated_project = projects_service.update_project(
        db=db, project_id=project_id, project_data=update_data, image_file=image
    )

    if updated_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return updated_project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    """Delete a project and its associated image."""
    db_project = projects_service.delete_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    return None
