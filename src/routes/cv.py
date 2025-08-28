from typing import Literal
from fastapi import APIRouter, Depends, UploadFile, File, status
from starlette.responses import StreamingResponse
import io

from services import cv_service
from dependencies import get_current_admin_user


router = APIRouter(prefix="/cv", tags=["CV / Resume"])

SUPPORTED_LANGUAGES = Literal["en", "es"]


@router.get(
    "/download/{lang_code}",
    summary="Download CV as PDF",
    description="Generates and downloads a PDF version of the CV in the specified language.",
)
def download_cv(lang_code: SUPPORTED_LANGUAGES):
    """
    Endpoint to download the CV in PDF format.

    - **lang_code**: Specify the language of the CV. Supported: `en`, `es`.
    """
    pdf_bytes = cv_service.generate_cv_pdf(lang_code=lang_code)
    filename = f"CV_Joaquin_{lang_code.upper()}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.put(
    "/upload/{lang_code}",
    status_code=status.HTTP_200_OK,
    summary="Update CV Markdown file",
    description="Uploads and replaces the Markdown source file for a CV in a specific language. Requires admin authentication.",
    dependencies=[Depends(get_current_admin_user)],
)
async def upload_cv(lang_code: SUPPORTED_LANGUAGES, file: UploadFile = File(...)):
    """
    Endpoint to upload and update a CV's .md file.

    - **lang_code**: Language of the CV to update ('en' or 'es').
    - **file**: The .md file to upload.
    """
    await cv_service.update_cv_md(lang_code=lang_code, file=file)
    return {"message": f"CV for language '{lang_code}' updated successfully."}