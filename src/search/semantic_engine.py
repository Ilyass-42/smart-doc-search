from sentence_transformers import SentenceTransformer
import numpy as np
from src.documents.chunk_model import Chunk
from src.preprocessing.vectorizer import cosine_similarity

class SemanticEngine:
    def __init__(self,list_chunks: list[Chunk]):
        self._model = SentenceTransformer("all-MiniLM-L6-v2")
        print("Model chargé")

        self._list_chunks = list_chunks
        self._embeddings = None

        if list_chunks:
            self._embeddings = self._model.encode(
                [c.content for c in list_chunks],
                normalize_embeddings=True
            )

    def add(self,list_chunks : list[Chunk]):
        self._list_chunks.extend(list_chunks)
    
        new_embeddings = self._model.encode(
            [c.content for c in list_chunks],
            normalize_embeddings=True
        )
        if self._embeddings is None:
            self._embeddings = new_embeddings
        else:
            self._embeddings = np.vstack([self._embeddings,new_embeddings])

    def search(self,query:str,k=3):

        k = min(k,len(self._list_chunks))

        query_embedding = self._model.encode(query,normalize_embeddings=True)
        scores = self._embeddings @ query_embedding
        
        top_k_idx = np.argsort(scores)[::-1][:k]

        return [(scores[i],self._list_chunks[i]) for i in top_k_idx]
    
    @property
    def list_chunks(self):
        return self._list_chunks
