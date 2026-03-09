# read_pdf.py — version corrigée avec chunking par fenêtre glissante
import fitz
import io
from fastapi import UploadFile

def read_pdf(file: UploadFile, chunk_size: int = 200, overlap: int = 30) -> list[str]:
    """
    Extrait le texte d'un PDF et le découpe en chunks de taille fixe
    avec chevauchement pour ne pas couper le sens entre deux chunks.
    
    :param chunk_size: nombre de mots par chunk
    :param overlap: nombre de mots partagés entre deux chunks consécutifs
    """
    pdf_in_memory = io.BytesIO(file.file.read())
    doc = fitz.open(stream=pdf_in_memory, filetype="pdf")

    # 1. Extraire tout le texte du document d'un coup
    full_text = ""
    for page in doc:
        full_text += page.get_text("text") + " "
    doc.close()

    # 2. Découper en mots et créer des chunks avec overlap
    words = full_text.split()
    chunks = []
    
    step = chunk_size - overlap  # pas d'avancement entre deux chunks
    
    for i in range(0, len(words), step):
        chunk_words = words[i : i + chunk_size]
        if len(chunk_words) < 20:  # ignorer les micro-chunks en fin de doc
            break
        chunks.append(" ".join(chunk_words))

    return chunks