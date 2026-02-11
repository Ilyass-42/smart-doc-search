from src.documents.chunk_model import Chunk
import re 
import nltk
import numpy as np

def build_vocabulary(chunks :list [Chunk]) -> list [str]:
    vocab = set()

    for chunk in chunks:
        mots_propre = process_text(chunk.content)
        vocab.update(mots_propre)
    return sorted(list(vocab))

def process_text(text:str)-> list[str]:
    mots = re.findall("[a-zA-Zàâéèêëïîôùûüÿç]+",text)

    mots = [mot.lower() for mot in mots]

    french_stop_word = nltk.corpus.stopwords.words('french')
    mots = [mot for mot in mots if mot not in french_stop_word]

    return mots

def TF(vocab:list[str], chunk : Chunk) -> list[int]:
    mots_chunks = process_text(chunk.content)
    vector = np.zeros(len(vocab))

    freq = {}
    for mot in mots_chunks:
        freq[mot] = freq.get(mot,0) +1

    for i,mot in enumerate(vocab):
        if mot in freq:
            vector[i] = freq[mot]
    return vector

def cosine_similarity(vect1,vect2)->int:
    norm1  =np.linalg.norm(vect1)
    norm2  =np.linalg.norm(vect2)
    
    if (norm1 == 0) or (norm2 ==0):
        return 0
    return np.dot(vect1,vect2)/(np.linalg.norm(vect1)*np.linalg.norm(vect2))




if __name__=="__main__":
    from src.documents.read_txt import read_txt_file
    from src.documents.build_chunks import build_chunks
    FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
    source ="example"
    chunk_texts = read_txt_file(FILEPATH)
    chunk_list = build_chunks(chunk_texts,source)
    vocab = build_vocabulary(chunk_list)
    print(f"===== Vocabulaire====\n {vocab}")
    print(f"=====TF===== \n{TF(vocab,chunk_list[0])}")
    print(chunk_list[0].content)


