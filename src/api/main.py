from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.search.engine import Engine
from src.documents.read_pdf import read_pdf
from src.documents.build_chunks import build_chunks
from src.search.semantic_engine import SemanticEngine


Engine = Engine(list_chunks=[]) 
Semantic = SemanticEngine(list_chunks=[])


app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "API Smart Doc Search est en marche 🚀"}

@app.post("/upload")
async def upload(file:UploadFile = File(...)):
    if  file.filename.endswith(".txt"):
        content = await file.read()
        text = content.decode("utf-8")

        paragraphs = [p for p in text.split("\n\n") if p.strip() != ""]
    elif file.filename.endswith(".pdf"):
        paragraphs = read_pdf(file)
    
    chunks_list = build_chunks(paragraphs,source=file.filename)
    Engine.add(chunks_list)
    Semantic.add(list_chunks=chunks_list)

    return {"message" :f"{len(chunks_list)} chunks ajoutés au moteur",
            "message2":f"Nombre total de chunks dans le moteur Engine: {len(Engine.list_chunks)}",
            "message3":f"Nombre total de chunks dans le moteur Semantic : {len(Semantic.list_chunks)}"
            }

            # "total_chunks TF-IDF":f"{len(Engine.list_chunks)} chunks ajoutés au moteur TF-IDF",
            # "total_chunks Semantic":f"{len(Semantic.list_chunks)}"} 


class SearchRequest(BaseModel):
    query : str
    k : int 

@app.post("/search")
def search (objet : SearchRequest):
    query = objet.query
    k = objet.k

    res = Engine.search(query,k)

    return [
        {"score":score, "chunk":chunk.content}
        for score,chunk in res
        ]

class SemanticSearchRequest(BaseModel):
    query : str
    k : int


@app.post("/semantic_search")
def semantic_search(request:SemanticSearchRequest):
    query = request.query
    k = request.k

    res = Semantic.search(query,k)

    return [
        {"score":float(score), "chunk":chunk.content}
        for score,chunk in res
        ]
    


    
