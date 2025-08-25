import os
import logging
from typing import Literal

import markdown2
from fastapi import HTTPException, status
from weasyprint import CSS, HTML

logger = logging.getLogger(__name__)

CV_DIR = "src/cv"
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
    md_filepath = os.path.join(CV_DIR, md_filename)
    css_filepath = os.path.join(CV_DIR, "style.css")

    # 1. Verify that the required files exist
    if not os.path.exists(md_filepath):
        logger.error(f"Markdown file not found: {md_filepath}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CV for language '{lang_code}' not found.",
        )
    if not os.path.exists(css_filepath):
        logger.error(f"Stylesheet not found: {css_filepath}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CV stylesheet is missing.",
        )

    try:
        # 2. Read Markdown and CSS content and convert to HTML
        with open(md_filepath, "r", encoding="utf-8") as f:
            html_content = markdown2.markdown(f.read(), extras=["tables", "fenced-code-blocks"])

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