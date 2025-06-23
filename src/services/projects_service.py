from sqlalchemy.orm import Session
from models.project import Project
from models.tag import Tag
from models.technology import Technology
from schemas import project as project_schema


def get_project(db: Session, project_id: int):
    return db.query(Project).filter(Project.id == project_id).first()


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Project).offset(skip).limit(limit).all()


def create_project(db: Session, project: project_schema.ProjectCreate):
    db_project = Project(
        name=project.name,
        image_url=project.image_url,
        link=project.link,
        source_code=project.source_code,
        interest=project.interest,
    )
    for tag_data in project.tags:
        db_tag = Tag(**tag_data.model_dump(), project=db_project)
        db.add(db_tag)

    for tech_data in project.technologies:
        db_tech = Technology(**tech_data.model_dump(), project=db_project)
        db.add(db_tech)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: project_schema.ProjectUpdate):
    db_project = get_project(db=db, project_id=project_id)
    if not db_project:
        return None

    update_data = project.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_project, key, value)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db=db, project_id=project_id)
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project
