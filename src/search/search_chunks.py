"""
Module qui permet de trouver les chunks si leurs contenus contient le mot recherché.
"""

from ..documents.chunk_model import Chunk

def search_chunks(chunks:list[Chunk], query :str, *querys) -> list[Chunk]:
    res = []
    querys = list(querys)
    if query=="" or ( "" in querys):
        return res
    query = query.lower()
    querys = [querry.lower() for querry in querys] 
    for chunk in chunks:
        for querry in querys:
            if query in chunk.content.lower() or querry in chunk.content.lower():
                if (chunk not in res):
                    res.append(chunk)
    return res

# idée pour chercher les phrases, on les decoupes en mots.

if __name__ == "__main__":
    from src.documents.build_chunks import build_chunks
    from src.documents.read_txt import read_txt_file
    FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
    source ="example"
    chunk_texts = read_txt_file(FILEPATH)
    chunk_list = build_chunks(chunk_texts,source)

    res = search_chunks(chunk_list,"cette","beer")
    print(res)
