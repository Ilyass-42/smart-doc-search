from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from src.search.engine import Engine
from src.documents.read_txt import read_txt_file
from src.documents.build_chunks import build_chunks



Engine = Engine(list_chunks=[]) 


app = FastAPI()

@app.get("/")
def read_root():
    return {"message" : "API Smart Doc Search est en marche 🚀"}

@app.post("/upload")
async def upload(file:UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        return {"error" : "Seuls les fichiers txt sont accéptés pour le moment"}
    
    content = await file.read()
    text = content.decode("utf-8")

    paragraphs = [p for p in text.split("\n\n") if p.strip() != ""]

    chunks_list = build_chunks(paragraphs,source=file.filename)

    Engine.add(chunks_list)

    return {"message" :f"{len(chunks_list)} chunks ajoutés au moteur", "total_chunks":len(Engine.list_chunks) }


class SearchRequest(BaseModel):
    querry : str
    k : int 

@app.post("/search")
def search (objet : SearchRequest):
    querry = objet.querry
    k = objet.k

    res = Engine.search(querry,k)

    return [
        {"score":score, "content":chunk.content}
        for score,chunk in res
        ]


    
