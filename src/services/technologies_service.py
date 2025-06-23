from sqlalchemy.orm import Session
from models import technology as technology_model
from schemas import technology as technology_schema


def get_technology(db: Session, technology_id: int):
    return (
        db.query(technology_model.Technology)
        .filter(technology_model.Technology.id == technology_id)
        .first()
    )


def get_technologies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(technology_model.Technology).offset(skip).limit(limit).all()


def create_technology(db: Session, technology: technology_schema.TechnologyCreate):
    db_technology = technology_model.Technology(**technology.model_dump())

    db.add(db_technology)
    db.commit()

    db.refresh(db_technology)

    return db_technology


def update_technology(
    db: Session, technology_id: int, technology_data: technology_schema.TechnologyUpdate
):

    db_technology = (
        db.query(technology_model.Technology)
        .filter(technology_model.Technology.id == technology_id)
        .first()
    )

    if not db_technology:
        return None

    update_data = technology_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_technology, key, value)

    db.commit()
    db.refresh(db_technology)

    return db_technology


def delete_technology(db: Session, technology_id: int):
    db_technology = (
        db.query(technology_model.Technology)
        .filter(technology_model.Technology.id == technology_id)
        .first()
    )

    if db_technology:
        db.delete(db_technology)
        db.commit()

    return db_technology
