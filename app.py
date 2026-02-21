import streamlit as st
import requests
import time


# if "uploaded_file_name" not in st.session_state:
#     st.session_state.uploaded_file_name = None

st.title("Smart Doc Search ")

engine_type = st.radio("Choisis le moteur :", ["TF-IDF","Semantic"])

upload_file = st.file_uploader("upload un fichier ", type =["txt","pdf"])



if upload_file is not None:
    response = requests.post(
            "http://127.0.0.1:8000/upload", 
            files={"file": upload_file}
    )    
    st.success(f"{response.json()['message']}")
    st.success(f"{response.json()['message2']}")
    st.success(f"{response.json()['message3']}")
        # st.session_state.uploaded_file_name = upload_file.name

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