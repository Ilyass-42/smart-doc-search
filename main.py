from src.search.engine import Engine
from src.documents.read_txt import read_txt_file
from src.documents.build_chunks import build_chunks


FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
source ="example"
chunk_texts = read_txt_file(FILEPATH)
chunk_list = build_chunks(chunk_texts,source)
Engine = Engine(chunk_list) 


while True:
    querry = input("Tapez votre requette (ou exit) :")
    
    if querry.lower() == "exit":
        break
    
    res = Engine.search(querry)

    for score, chunks in res:
        print(f"Score : {score:.4f}\n")
        print(f"Chunks : {chunks}\n")

