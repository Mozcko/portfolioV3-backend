from sqlalchemy.orm import Session
from models.experience import Experience
from schemas import experience as experience_schema


def get_experience(db: Session, experience_id: int):
    return db.query(Experience).filter(Experience.id == experience_id).first()


def get_experiences(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Experience).offset(skip).limit(limit).all()


def create_experience(db: Session, experience: experience_schema.ExperienceCreate):
    db_experience = Experience(**experience.model_dump())
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


def update_experience(
    db: Session, experience_id: int, experience_data: experience_schema.ExperienceUpdate
):
    db_experience = get_experience(db, experience_id)
    if not db_experience:
        return None

    update_data = experience_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_experience, key, value)

    db.commit()
    db.refresh(db_experience)
    return db_experience


def delete_experience(db: Session, experience_id: int):
    db_experience = get_experience(db, experience_id)
    if not db_experience:
        return None
    db.delete(db_experience)
    db.commit()
    return db_experience
