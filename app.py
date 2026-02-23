import streamlit as st
import requests
import time
from sentence_transformers import SentenceTransformer

def afficher_reponse(reponse:str):
    st.subheader("Réponse de l'assistant")
    st.markdown(reponse)

def appel_llm(prompt):
    return "Testna"

def construire_prompt(top_chunks,user_question:str)->str:
    """ fonction qui va contruire un prompt en fonction de top chunks et de la question de l'utilisateur
    ici top_chunks est un json qui contient les scores ainsi que le contenu des chunks
    """
    sources_text =""
    for i,c in enumerate(top_chunks,start=1):
        sources_text+=f"[Chunk {i}] {c['chunk']}\n\n"
        
    return f"Tu es un assistant IA expert en documents. Tu dois répondre uniquement en utilisant les sources fournies ci-dessous. Sources :\n\n{ sources_text} Question : {user_question} \n\nInstructions :\n\n1. Réponds uniquement à partir des sources ci-dessus. \n\n2. Si l'information n'est pas présente, réponds : Je n'ai pas assez de ressources pour répondre. \n\n3. Cite les sources utilisées dans ta réponse, par exemple [Chunk 2]. \n\n4. Garde la réponse claire et synthétique, et si possible, utilise des bullet points pour structurer l’information."

    

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

st.title("Smart Doc Search ")

upload_file = st.file_uploader("upload un fichier ", type =["txt","pdf"])
if upload_file is not None:
    response = requests.post(
            "http://127.0.0.1:8000/upload", 
            files={"file": upload_file}
    )    
    st.success(f"{response.json()['message']}")
    st.success(f"{response.json()['message2']}")
    st.success(f"{response.json()['message3']}")
    st.session_state.uploaded_file_name = upload_file.name


mode = st.radio("Choisis le mode :",["Recherche simple", "Assistant IA"])

if mode == "Recherche simple":
    engine_type = st.radio("Choisis le moteur :", ["TF-IDF","Semantic"])

    query = st.text_input("Votre requete :")
    k = st.number_input("Nombre de résultat :")

    debut = time.time() 
    if st.button("Rechercher") and query:
        endpoint = "http://127.0.0.1:8000/search" if engine_type == "TF-IDF" else "http://127.0.0.1:8000/semantic_search"

        res = requests.post(endpoint, json={"query": query, "k": k}).json()
        fin = time.time()
        st.subheader("Résultats")
        for r in res:
            st.markdown(f"**Score:** {r['score']:.3f}")
            st.markdown(f"{r['chunk']}")
            st.write("---")
        st.write(f"Temps écoulé : {fin-debut}")


elif mode == "Assistant IA":
    st.header("Assistant IA sur vos documents")

    user_question = st.text_input("Posez votre question :")
    k=5
    endpoint = "http://127.0.0.1:8000/semantic_search"

    debut = time.time()
    if st.button("Poser la question") and user_question:
        top_chunks = requests.post(endpoint,json={"query":user_question, "k":k}).json()
        
        prompt = construire_prompt(top_chunks,user_question)

        reponse = appel_llm(prompt)
        afficher_reponse(reponse)
        st.write(f"Temps écoulé : {time.time()-debut}")