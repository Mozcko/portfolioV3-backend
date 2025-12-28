from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schemas import tag as tag_schema
from src.services import tags_service
from src.dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/tags", tags=["Tags"])

@router.post("/", response_model=tag_schema.Tag, status_code=status.HTTP_201_CREATED, dependencies=[Depends(get_current_admin_user)])
def create_tag(tag: tag_schema.TagCreate, db: Session = Depends(get_db)):
    return tags_service.create_tag(db=db, tag=tag)

@router.get("/", response_model=List[tag_schema.Tag])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return tags_service.get_tags(db=db, skip=skip, limit=limit)

@router.get("/{tag_id}", response_model=tag_schema.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = tags_service.get_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return db_tag

@router.put("/{tag_id}", response_model=tag_schema.Tag, dependencies=[Depends(get_current_admin_user)])
def update_tag(tag_id: int, tag: tag_schema.TagUpdate, db: Session = Depends(get_db)):
    db_tag = tags_service.update_tag(db=db, tag_id=tag_id, tag_data=tag)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return db_tag

@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(get_current_admin_user)])
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = tags_service.delete_tag(db=db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return None
