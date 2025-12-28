from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List
from src.models.tag import Tag
from src.schemas import tag as tag_schema

def get_tag(db: Session, tag_id: int):
    return db.query(Tag).filter(Tag.id == tag_id).first()

def get_tags(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tag).offset(skip).limit(limit).all()

def create_tag(db: Session, tag: tag_schema.TagCreate) -> Tag:
    db_tag = Tag(**tag.model_dump())
    db.add(db_tag)
    try:
        db.commit()
        db.refresh(db_tag)
        return db_tag
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tag with this name already exists"
        )

def update_tag(db: Session, tag_id: int, tag_data: tag_schema.TagUpdate) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    
    update_data = tag_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_tag, key, value)

    db.commit()
    db.refresh(db_tag)
    return db_tag

def delete_tag(db: Session, tag_id: int) -> Optional[Tag]:
    db_tag = get_tag(db, tag_id)
    if not db_tag:
        return None
    db.delete(db_tag)
    db.commit()
    return db_tag
