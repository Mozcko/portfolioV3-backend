from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import experience as experience_schema
from services import experiences_service
from dependencies import get_db, get_current_admin_user
from utils import save_image 

router = APIRouter(prefix="/experiences", tags=["Experiences"])

@router.post("/", response_model=experience_schema.Experience, dependencies=[Depends(get_current_admin_user)])
def create_experience(
    db: Session = Depends(get_db),
    title: str = Form(...),
    company_name: str = Form(...),
    icon_bg: str = Form(...),
    date: str = Form(...),
    points: str = Form(...),
    icon_file: UploadFile = File(..., alias="icon") 
):
    
    icon_url = save_image(icon_file)

    
    experience_data = experience_schema.ExperienceCreate(
        title=title,
        company_name=company_name,
        icon_bg=icon_bg,
        date=date,
        points=points,
        icon=icon_url 
    )
    
    return experiences_service.create_experience(db=db, experience=experience_data)

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
def update_experience(
    experience_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    company_name: Optional[str] = Form(None),
    icon_bg: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    points: Optional[str] = Form(None),
    icon_file: Optional[UploadFile] = File(None, alias="icon")
):
    update_data = {}
    if title is not None: update_data['title'] = title
    if company_name is not None: update_data['company_name'] = company_name
    if icon_bg is not None: update_data['icon_bg'] = icon_bg
    if date is not None: update_data['date'] = date
    if points is not None: update_data['points'] = points

    if icon_file:
        icon_url = save_image(icon_file)
        update_data['icon'] = icon_url

    if not update_data:
        raise HTTPException(status_code=400, detail="No hay datos para actualizar")
    
    experience_update_schema = experience_schema.ExperienceUpdate(**update_data)

    db_experience = experiences_service.update_experience(
        db, experience_id=experience_id, experience_data=experience_update_schema
    )
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience

@router.delete("/{experience_id}", response_model=experience_schema.Experience, dependencies=[Depends(get_current_admin_user)])
def delete_experience(experience_id: int, db: Session = Depends(get_db)):
    db_experience = experiences_service.delete_experience(db, experience_id=experience_id)
    if db_experience is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    return db_experience