import logging
from typing import Literal

import markdown2
from fastapi import HTTPException, status, UploadFile
from weasyprint import CSS, HTML

from core.config import SRC_DIR

logger = logging.getLogger(__name__)

CV_DIR = SRC_DIR / "static" / "others"
SUPPORTED_LANGUAGES = Literal["en", "es"]


def generate_cv_pdf(lang_code: SUPPORTED_LANGUAGES) -> bytes:
    """
    Generates a PDF version of the CV from a Markdown file.

    Args:
        lang_code: The language code ('en' or 'es').

    Returns:
        The generated PDF as bytes.

    Raises:
        HTTPException: If the Markdown or CSS file is not found.
    """
    md_filename = f"cv_{lang_code}.md"
    md_filepath = CV_DIR / md_filename
    css_filepath = CV_DIR / "style.css"

    # 1. Verify that the required files exist
    if not md_filepath.exists():
        logger.error(f"Markdown file not found: {md_filepath}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV for language '{lang_code}' not found.",
        )
    if not css_filepath.exists():
        logger.error(f"Stylesheet not found: {css_filepath}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CV stylesheet is missing.",
        )

    try:
        # 2. Read Markdown and CSS content and convert to HTML
        html_content = markdown2.markdown(
            md_filepath.read_text(encoding="utf-8"),
            extras=["tables", "fenced-code-blocks"],
        )

        # 3. Generate PDF using WeasyPrint
        html = HTML(string=html_content)
        css = CSS(css_filepath)
        pdf_bytes = html.write_pdf(stylesheets=[css])

        logger.info(f"Successfully generated PDF for CV in '{lang_code}'.")
        return pdf_bytes

    except Exception as e:
        logger.exception(f"Failed to generate PDF for CV '{lang_code}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not generate the PDF file.",
        )


async def update_cv_md(lang_code: SUPPORTED_LANGUAGES, file: UploadFile):
    """
    Updates a CV's Markdown file with the content of an uploaded file.

    Args:
        lang_code: The language code ('en' or 'es').
        file: The uploaded Markdown file.

    Raises:
        HTTPException: If the uploaded file is not a Markdown file or if
                       there's an error saving the file.
    """
    if not file.filename.endswith(".md"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload a Markdown (.md) file.",
        )

    md_filepath = CV_DIR / f"cv_{lang_code}.md"

    try:
        content = await file.read()
        md_filepath.write_text(content.decode("utf-8"), encoding="utf-8")
        logger.info(f"Successfully updated CV markdown for '{lang_code}'.")
    except Exception as e:
        logger.exception(f"Failed to update CV markdown for '{lang_code}': {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not save the CV file.",
        )