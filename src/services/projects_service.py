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
    technology_ids = project.technology_ids

    project_data = project.model_dump(exclude={"tags", "technology_ids"})
    db_project = Project(**project_data)

    for tag_data in project.tags:
        db_tag = Tag(**tag_data.model_dump())
        db_project.tags.append(db_tag)

    if technology_ids:
        db_technologies = (
            db.query(Technology).filter(Technology.id.in_(technology_ids)).all()
        )
        if len(db_technologies) != len(technology_ids):
            # Opcional: Podrías querer manejar este error de forma más específica.
            # Por ahora, simplemente ignoramos los IDs no encontrados.
            pass
        db_project.technologies.extend(db_technologies)

    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: project_schema.ProjectUpdate):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        return None

    update_data = project.model_dump(
        exclude_unset=True, exclude={"tags", "technology_ids"}
    )
    for key, value in update_data.items():
        setattr(db_project, key, value)

    if project.technology_ids is not None:
        db_project.technologies.clear()
        if project.technology_ids:
            db_technologies = (
                db.query(Technology)
                .filter(Technology.id.in_(project.technology_ids))
                .all()
            )
            db_project.technologies.extend(db_technologies)

    if project.tags is not None:
        db_project.tags.clear()
        for tag_data in project.tags:
            db_tag = Tag(**tag_data.model_dump())
            db_project.tags.append(db_tag)

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
