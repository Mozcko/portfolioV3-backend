from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from schemas import experience as experience_schema
from services import experiences_service
from dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/experiences", tags=["Experiences"])

@router.post("/", response_model=experience_schema.ExperienceCreate, dependencies=[Depends(get_current_admin_user)])
def create_experience(experience: experience_schema.ExperienceCreate, db: Session = Depends(get_db)):
    return experiences_service.create_experience(db=db, experience=experience)

@router.get("/", response_model=List[experience_schema.Experience])
def read_experiences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    experiences = experiences_service.get_experiences(db, skip=skip, limit=limit)
    return experiences

@router.get("/{experience_id}", response_model=experience_schema.Experience)
def read_experience(experience_id: int, db: Session = Depends(get_db)):
    db_experience = experiences_service.get_experience(db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@router.put("/{experience_id}", response_model=experience_schema.Experience, dependencies=[Depends(get_current_admin_user)])
def update_experience(experience_id: int, experience: experience_schema.ExperienceUpdate, db: Session = Depends(get_db)):
    db_experience = experiences_service.update_experience(db, experience_id=experience_id, experience_data=experience)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@router.delete("/{experience_id}", response_model=experience_schema.Experience, dependencies=[Depends(get_current_admin_user)])
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    db_experience = experiences_service.delete_experience(db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience