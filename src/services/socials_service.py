from sqlalchemy.orm import Session
from fastapi import UploadFile
from typing import Optional, List

from src.models.social import Social
from src.schemas import social as social_schema
from src.utils import save_image, delete_image


def get_social(db: Session, social_id: int) -> Optional[Social]:
    """Get a single social profile by ID."""
    return db.query(Social).filter(Social.id == social_id).first()


def get_socials(db: Session, skip: int = 0, limit: int = 100) -> List[Social]:
    """Get all social profiles."""
    return db.query(Social).offset(skip).limit(limit).all()


def create_social(
    db: Session, social_data: social_schema.SocialCreate, image_file: UploadFile
) -> Social:
    """
    Creates a social profile, saves its image, and returns the DB object.
    """
    image_route = save_image(image_file)

    db_social = Social(**social_data.model_dump(), image_route=image_route)

    db.add(db_social)
    db.commit()
    db.refresh(db_social)
    return db_social


def update_social(
    db: Session,
    social_id: int,
    social_data: social_schema.SocialUpdate,
    image_file: Optional[UploadFile] = None,
) -> Optional[Social]:
    """
    Updates a social profile. If a new image is provided,
    it replaces the old one.
    """
    db_social = get_social(db, social_id)
    if not db_social:
        return None

    update_data = social_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if value is not None:
            setattr(db_social, key, value)

    if image_file:
        if db_social.image_route:
            delete_image(db_social.image_route)

        new_image_route = save_image(image_file)
        db_social.image_route = new_image_route

    db.commit()
    db.refresh(db_social)
    return db_social


def delete_social(db: Session, social_id: int) -> Optional[Social]:
    """Deletes a social profile and its associated image."""
    db_social = get_social(db, social_id)
    if not db_social:
        return None

    if db_social.image_route:
        delete_image(db_social.image_route)

    db.delete(db_social)
    db.commit()
    return db_social