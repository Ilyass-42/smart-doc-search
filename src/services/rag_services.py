from src.services.retrieval_services import RetrievalService
from google import genai
import os
from dotenv import load_dotenv
 
load_dotenv()
KEY = os.getenv("KEY")
client = genai.Client(api_key=KEY) 

class RAGService:
    def __init__(self, retrieval_service: RetrievalService, k=5, token_limit=1500):
        self.retrieval_service = retrieval_service
        self.k = k
        self.token_limit = token_limit

    def construct_prompt(self, top_chunks, question):
        sources_text = ""
        for i, (_, c) in enumerate(top_chunks, 1):
            sources_text += f"[Chunk {i}] {c.content}\n\n"

        return f"""
Tu es un assistant IA expert en documents. Tu dois répondre uniquement en utilisant les sources fournies ci-dessous. 
Sources :
{sources_text}

Question : {question}

Instructions :
1. Réponds uniquement à partir des sources ci-dessus.
2. Si l'information n'est pas présente, réponds : Je n'ai pas assez de ressources pour répondre.
3. Cite les sources utilisées, par exemple [Chunk 2].
4. Garde la réponse claire et synthétique, utilise des bullet points si possible.
5. Fusionne les infos similaires et réponds dans la langue de la question.
"""

    def ask(self, question):
        top_chunks = self.retrieval_service.search_semantic(question, self.k)

        filtred_chunks = []
        total_tokens = 0
        for score,chunk in top_chunks:
            tokens = len(chunk.content.split())
            if total_tokens + tokens > self.token_limit:
                break
            filtred_chunks.append((score,chunk))
            total_tokens += tokens

        prompt = self.construct_prompt(filtred_chunks, question)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents = prompt,
        )

        answer_text = response.text

        return {"answer": answer_text, "sources": [c.id for _, c in filtred_chunks]}