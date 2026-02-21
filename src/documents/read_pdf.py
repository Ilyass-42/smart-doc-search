import fitz
import io
from fastapi import UploadFile


def read_pdf(file:UploadFile)->list[str]:
    """Extrait les pargraphes d'un fichier pdf."""

    pdf_in_memory = io.BytesIO(file.file.read())
    doc = fitz.open(stream=pdf_in_memory, filetype="pdf")

    paragraphs = []
    for page in doc:
        text = page.get_text("text")
        page_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        paragraphs.extend(page_paragraphs)
    
    doc.close()
    return paragraphs