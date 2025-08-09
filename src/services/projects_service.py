from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional

from models.project import Project  
from schemas import project as project_schema

from utils import save_image, delete_image

def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()

def create_project(db: Session, project: project_schema.ProjectCreate, image_file: UploadFile) -> Project:
    """
    Crea un proyecto, guarda su imagen y devuelve el objeto de la BD.
    """
    # 1. Guardar la imagen y obtener la ruta
    image_route = save_image(image_file)
    
    # 2. Crear el objeto del modelo con los datos y la ruta de la imagen
    db_project = Project(
        **project.model_dump(),
        image_route=image_route
    )
    
    # 3. Guardar en la base de datos
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
    Actualiza un proyecto. Si se proporciona una nueva imagen,
    reemplaza la anterior.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None

    # Actualizar los campos del proyecto
    update_data = project_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_project, key, value)

    # Si se subió un archivo nuevo
    if image_file:
        # 1. Borrar la imagen antigua
        if db_project.image_route:
            delete_image(db_project.image_route)
        
        # 2. Guardar la imagen nueva y actualizar la ruta
        new_image_route = save_image(image_file)
        db_project.image_route = new_image_route

    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> Optional[Project]:
    """
    Elimina un proyecto y su imagen asociada.
    """
    db_project = get_project(db, project_id)
    if not db_project:
        return None
        
    # 1. Borrar la imagen del servidor
    if db_project.image_route:
        delete_image(db_project.image_route)
        
    # 2. Borrar el registro de la base de datos
    db.delete(db_project)
    db.commit()
    return db_project
