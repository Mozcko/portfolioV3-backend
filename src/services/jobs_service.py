from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional

from ..models.job import Job
from ..schemas import job as job_schema
from ..utils import save_image, delete_image


def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()


def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()


def create_job(
    db: Session, job_data: job_schema.JobCreate, image_file: UploadFile
) -> Job:
    image_route = save_image(image_file)

    db_job = Job(**job_data.model_dump(), image_route=image_route)

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(
    db: Session,
    job_id: int,
    job_data: job_schema.JobUpdate,
    image_file: Optional[UploadFile] = None,
) -> Optional[Job]:

    db_job = get_job(db, job_id)

    if not db_job:
        return None

    update_data = job_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_job, key, value)

    if image_file:
        if db_job.image_route:
            delete_image(db_job.image_route)

        new_image_route = save_image(image_file)
        db_job.image_route = new_image_route

    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int) -> Optional[Job]:

    db_job = get_job(db=db, job_id=job_id)

    if not db_job:
        return None

    if db_job.image_route:
        delete_image(db_job.image_route)

    db.delete(db_job)
    db.commit()
    return db_job
