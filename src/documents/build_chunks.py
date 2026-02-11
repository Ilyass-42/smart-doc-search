"""
Module Chunks.py qui permet de generer les chunks a partir de texts nettoyés.
"""
from .chunk_model import Chunk
from typing import List

def build_chunks(chunk_texts: List[str],source: str)-> List[Chunk]:
    """
    Transforme une liste de textes en une liste de chunks
    
    - Ignore les textes vides
    - Assigne un ordre à chaque Chunk
    - Génere un id de chaque CHunk

    :param chunk_texts: Textes nettoyés
    :type chunk_texts: List[str]
    :param source: Source du texte
    :type source: str
    :return: Liste d'objets de Chunk
    :rtype: List[Chunk]
    """
    ordre = 0 
    chunks = []
    for texte in chunk_texts:
        if len(texte) != 0:
            id_chunk = f"{source}" +f"_{ordre}"
            chunks.append(Chunk(id_chunk,texte,source,ordre))
            ordre +=1
    return chunks


if __name__ =="__main__":
    from src.documents.read_txt import read_txt_file
    FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
    source ="example"
    chunk_texts = read_txt_file(FILEPATH)
    chunk_list = build_chunks(chunk_texts,source)
    for chunk in chunk_list:
        print(chunk)
