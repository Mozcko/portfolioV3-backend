from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile, status
from sqlalchemy.orm import Session
from typing import List, Optional

from src.schemas import social as social_schema
from src.services import socials_service
from src.dependencies import get_db, get_current_admin_user

router = APIRouter(prefix="/socials", tags=["Socials"])


@router.post(
    "/",
    response_model=social_schema.Social,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_admin_user)],
    summary="Create a new social profile",
)
def create_social(
    name: str = Form(...),
    link: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Creates a new social profile with its icon.
    """
    social_create = social_schema.SocialCreate(name=name, link=link)

    return socials_service.create_social(
        db=db, social_data=social_create, image_file=file
    )


@router.get(
    "/", response_model=List[social_schema.Social], summary="Get all social profiles"
)
def read_socials(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Gets a list of all social profiles.
    """
    return socials_service.get_socials(db, skip=skip, limit=limit)


@router.get(
    "/{social_id}", response_model=social_schema.Social, summary="Get a single social profile"
)
def read_social(social_id: int, db: Session = Depends(get_db)):
    """
    Gets a social profile by its ID.
    """
    db_social = socials_service.get_social(db, social_id=social_id)
    if db_social is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Social profile not found"
        )
    return db_social


@router.put(
    "/{social_id}",
    response_model=social_schema.Social,
    dependencies=[Depends(get_current_admin_user)],
    summary="Update a social profile",
)
def update_social(
    social_id: int,
    db: Session = Depends(get_db),
    name: Optional[str] = Form(None),
    link: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Updates a social profile. Allows changing data and/or the icon.
    """
    update_data = social_schema.SocialUpdate(name=name, link=link)

    if not update_data.model_dump(exclude_unset=True) and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data to update",
        )

    updated_social = socials_service.update_social(
        db=db, social_id=social_id, social_data=update_data, image_file=file
    )

    if updated_social is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Social profile not found"
        )

    return updated_social


@router.delete(
    "/{social_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin_user)],
    summary="Delete a social profile",
)
def delete_social(social_id: int, db: Session = Depends(get_db)):
    """
    Deletes a social profile and its associated icon.
    """
    db_social = socials_service.delete_social(db=db, social_id=social_id)
    if db_social is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Social profile not found"
        )

    return None