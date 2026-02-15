from src.documents.chunk_model import Chunk
import re 
import nltk
import numpy as np
from nltk.stem.snowball import FrenchStemmer
stemmer = FrenchStemmer()

def build_vocabulary(chunks :list [Chunk]) -> list [str]:
    """
    Prends en entrée une liste de chunk et en sortie donne une liste de string qui compse le vocabulaire associé au document
    """
    vocab = set()

    for chunk in chunks:
        mots_propre = process_text(chunk.content)
        mots_propre = normalize(chunk.content)
        vocab.update(mots_propre)
    return sorted(list(vocab))

def process_text(text:str)-> list[str]:
    """
    Prends une liste de chaine de caractére, mets en minuscule et enleve les mots répetitifs qui n'ont aucune valeurs (ex: le, la, de ....)
    """
    mots = re.findall("[a-zA-Zàâéèêëïîôùûüÿç]+",text)

    mots = [mot.lower() for mot in mots]

    french_stop_word = nltk.corpus.stopwords.words('french')
    mots = [mot for mot in mots if mot not in french_stop_word]

    return mots


def normalize(text: str):
    text = text.lower()                       # tout en minuscules
    text = re.sub(r'[^\w\s]', '', text)      # enlever la ponctuation
    words = text.split()
    words = [stemmer.stem(w) for w in words] # racines
    return words

def TF(word_to_index, content):
    vector = np.zeros(len(word_to_index))
    words = normalize(content)
    for mot in words:
        if mot in word_to_index:
            vector[word_to_index[mot]] += 1
    return vector






def cosine_similarity(vect1,vect2)->float:
    norm1  =np.linalg.norm(vect1)
    norm2  =np.linalg.norm(vect2)
    
    if (norm1 == 0) or (norm2 ==0):
        return 0
    return np.dot(vect1,vect2)/(np.linalg.norm(vect1)*np.linalg.norm(vect2))




# if __name__=="__main__":
#     from src.documents.read_txt import read_txt_file
#     from src.documents.build_chunks import build_chunks
#     FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
#     source ="example"
#     chunk_texts = read_txt_file(FILEPATH)
#     chunk_list = build_chunks(chunk_texts,source)
#     vocab = build_vocabulary(chunk_list)
#     print(f"===== Vocabulaire====\n {vocab}")
#     print(f"=====TF===== \n{TF(vocab,chunk_list[0])}")
#     print(chunk_list[0].content)


