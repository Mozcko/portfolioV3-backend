from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.schemas import job as job_schema
from src.services import jobs_service
from src.dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/",
    response_model=job_schema.Job,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
)
def create_job(
    title: str = Form(...),
    start_date: str = Form(...),
    end_date: Optional[str] = Form(None),
    current_job: bool = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    job_create = job_schema.JobCreate(
        title=title, start_date=start_date, end_date=end_date, current_job=current_job
    )

    return jobs_service.create_job(db=db, job_data=job_create, image_file=file)


@router.get("/", response_model=List[job_schema.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return jobs_service.get_jobs(db=db, skip=skip, limit=limit)


@router.get("/{job_id}", response_model=job_schema.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    db_job = jobs_service.get_job(db=db, job_id=job_id)

    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="trabajo no encontrado"
        )

    return db_job


@router.put(
    "/{job_id}",
    response_model=job_schema.Job,
    dependencies=[Depends(get_current_admin_user)],
)
def update_job(
    job_id: int,
    db: Session = Depends(get_db),
    title: Optional[str] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    current_job: Optional[bool] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    update_data = job_schema.JobUpdate(
        title=title, start_date=start_date, end_date=end_date, current_job=current_job
    )

    if not update_data.model_dump(exclude_unset=True) and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no hay datos para actualizar",
        )

    updated_job = jobs_service.update_job(
        db=db,
        job_id=job_id,
        job_data=update_data,
        image_file=file,
    )

    if updated_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no se encontró el trabajo"
        )

    return updated_job


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    db_job = jobs_service.delete_job(db=db, job_id=job_id)

    if db_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="no se encontró el trabajo"
        )

    return None
