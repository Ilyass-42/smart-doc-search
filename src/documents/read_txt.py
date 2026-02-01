"""
Module pour lire un fichier txt et découpe en une liste de chaine de caractéres (chunks).
"""
from typing import List
import os



def read_txt_file(filepath : str) -> List[str] :
    """
    Lit un fichier txt et découpe en une liste de chaine de caractéres (chunks).
    :param filepath: Chemin du fichier txt.
    :type filepath: str
    :return: une liste de chunks
    :rtype: List[str]
    """
    if not os.path.exists(filepath):
        print(f"Fichier introuvable : {filepath}")
    with open(filepath,'r',encoding='utf-8') as file_obj:
        content = file_obj.read()
    return clean_chunk(content.split("\n\n"))


def clean_chunk(chunks:List[str]) -> List[str]:
    """
    fonction qui nettoie les chunks des espaces.
    :param chunk: Liste de chaine de caractéres (chunk)
    :type chunk: List[str]
    :return: Une liste de chaines de caractéres sans espaces.
    :rtype: List[str]
    """
    for index, in enumerate(chunks):
        chunks[index] = chunks[index].strip()
    return chunks


if __name__ == "__main__":
    FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
    contenu = read_txt_file(FILEPATH)
    print(contenu)
