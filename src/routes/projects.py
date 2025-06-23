import json
from fastapi import APIRouter, Depends, HTTPException, status, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import project as project_schema
from services import projects_service
from dependencies import get_db, get_current_admin_user
from utils import save_image

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=project_schema.Project, dependencies=[Depends(get_current_admin_user)])
def create_project(
    db: Session = Depends(get_db),
    name: str = Form(...),
    interest: str = Form(...),
    link: Optional[str] = Form(None),
    source_code: Optional[str] = Form(None),
    tags: str = Form('[]'),
    technology_ids: str = Form('[]'),
    image_file: UploadFile = File(..., alias="image")
):
    image_url = save_image(image_file)

    try:
        tags_data = json.loads(tags)
        tech_ids_list = json.loads(technology_ids)
        if not all(isinstance(i, int) for i in tech_ids_list):
            raise HTTPException(status_code=400, detail="technology_ids debe ser una lista de enteros.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Formato JSON inválido para 'tags' o 'technology_ids'")

    project_data = project_schema.ProjectCreate(
        name=name,
        interest=interest,
        link=link,
        source_code=source_code,
        image_url=image_url,
        tags=tags_data,
        technology_ids=tech_ids_list
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
    name: Optional[str] = Form(None),
    interest: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    source_code: Optional[str] = Form(None),
    image_file: Optional[UploadFile] = File(None, alias="image")
):
    update_data = {}
    if name is not None: update_data['name'] = name
    if interest is not None: update_data['interest'] = interest
    if link is not None: update_data['link'] = link
    if source_code is not None: update_data['source_code'] = source_code

    if image_file:
        image_url = save_image(image_file)
        update_data['image_url'] = image_url

    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")

    project_update_schema = project_schema.ProjectUpdate(**update_data)
    
    db_project = projects_service.update_project(
        db=db, project_id=project_id, project=project_update_schema
    )
    if db_project is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return db_project

@router.delete("/{project_id}", response_model=project_schema.Project, dependencies=[Depends(get_current_admin_user)])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = projects_service.delete_project(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project