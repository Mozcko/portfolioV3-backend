from typing import Literal
from fastapi import APIRouter
from starlette.responses import StreamingResponse
import io

from services import cv_service

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
    filename = f"CV_Mozcko_{lang_code.upper()}.pdf"
    
    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )