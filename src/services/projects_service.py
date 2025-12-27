from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException, status
from typing import Optional, List

from src.models.project import Project
from src.models.technology import Technology
from src.schemas import project as project_schema

from src.utils import save_image, delete_image

def get_project(db: Session, project_id: int):
    """Get a single project with its technologies loaded."""
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    """Get all projects with their technologies loaded."""
    return db.query(Project).offset(skip).limit(limit).all()

def validate_technology_ids(db: Session, technology_ids: List[int]) -> List[Technology]:
    """Validate that all technology IDs exist and return the technology objects."""
    if not technology_ids:
        return []
    
    technologies = db.query(Technology).filter(Technology.id.in_(technology_ids)).all()
    
    if len(technologies) != len(technology_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more technology IDs are invalid"
        )
    
    return technologies

def create_project(
    db: Session, 
    project: project_schema.ProjectCreate, 
    image_file: UploadFile
) -> Project:
    """
    Create a new project with associated technologies.
    """
    # Validate technology IDs
    technologies = validate_technology_ids(db, project.technology_ids or [])
    
    # Save image and get route
    image_route = save_image(db, image_file)
    
    # Create project
    db_project = Project(
        title=project.title,
        description_en=project.description_en,
        description_es=project.description_es,
        image_route=image_route
    )
    
    # Associate technologies
    db_project.technologies = technologies
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(
    db: Session, 
    project_id: int, 
    project_data: project_schema.ProjectUpdate, 
    image_file: Optional[UploadFile] = None
) -> Optional[Project]:
    """
    Update a project including its technology associations.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    
    # Update basic fields
    update_data = project_data.model_dump(exclude_unset=True)
    
    # Handle technology updates separately
    technology_ids = update_data.pop('technology_ids', None)
    
    for key, value in update_data.items():
        if value is not None:
            setattr(db_project, key, value)

    # Update technologies if provided
    if technology_ids is not None:
        technologies = validate_technology_ids(db, technology_ids)
        db_project.technologies = technologies
    
    # Handle image update
    if image_file:
        if db_project.image_route:
            delete_image(db, db_project.image_route)
        new_image_route = save_image(db, image_file)
        db_project.image_route = new_image_route
    
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> Optional[Project]:
    """
    Delete a project and its associated image.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None
        
    # Delete image
    if db_project.image_route:
        delete_image(db, db_project.image_route)
        
    db.delete(db_project)
    db.commit()
    return db_project
