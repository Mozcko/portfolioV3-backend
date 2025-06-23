from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import project as project_schema
from services import projects_service
from dependencies import get_db, get_current_admin_user
from utils import save_image

router = APIRouter(prefix="/projects", tags=["Projects"])

router.post("/", response_model=project_schema.Project, dependencies=[Depends(get_current_admin_user)])
def create_project(
    db: Session = Depends(get_db),
    title: str = Form(...),
    description: str = Form(...),
    link: Optional[str] = Form(None),
    repository: Optional[str] = Form(None),
    file: UploadFile = File(...)  
):
    image_url = save_image(file)

    project_data = project_schema.ProjectCreate(
        title=title,
        description=description,
        image_url=image_url,
        link=link,
        repository=repository
    )
    
    return projects_service.create_project(db=db, project=project_data)

@router.get("/", response_model=List[project_schema.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = projects_service.get_projects(db, skip=skip, limit=limit)
    return projects


@router.get("/{project_id}", response_model=project_schema.Project)
def read_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_service.get_project(db=db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@router.put("/{project_id}", response_model=project_schema.Project, dependencies=[Depends(get_current_admin_user)])
def update_project(
    project_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    repository: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None) # El archivo es opcional en la actualización
):
    db_project = projects_service.get_project(db, project_id=project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")

    update_data = {
        "title": title,
        "description": description,
        "link": link,
        "repository": repository
    }
    update_data_filtered = {k: v for k, v in update_data.items() if v is not None}

    if file:
        image_url = save_image(file)
        update_data_filtered['image_url'] = image_url

    if not update_data_filtered:
        raise HTTPException(status_code=400, detail="No data provided for update")

    project_update_schema = project_schema.ProjectUpdate(**update_data_filtered)
    
    return projects_service.update_project(db, project_id=project_id, project_data=project_update_schema)


@router.delete("/{project_id}", response_model=project_schema.Project, dependencies=[Depends(get_current_admin_user)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_service.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project