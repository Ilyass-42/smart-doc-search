from src.search.engine import Engine
from src.search.semantic_engine import SemanticEngine

class RetrievalService:
    def __init__(self):
        self.tfidf_engine = Engine(list_chunks=[])
        self.semantic_engine = SemanticEngine(list_chunks=[])

    def add_chunks(self, chunks):
        self.tfidf_engine.add(chunks)
        self.semantic_engine.add(list_chunks=chunks)

    def search_tfidf(self, query, k):
        return self.tfidf_engine.search(query, k)

    def search_semantic(self, query, k):
        return self.semantic_engine.search(query, k)