from src.documents.chunk_model import Chunk
from src.preprocessing.vectorizer import build_vocabulary
from src.preprocessing.vectorizer import TF
from src.preprocessing.vectorizer import cosine_similarity


import numpy as np


class Engine:
    def __init__(self,list_chunks:list[Chunk]):
        self._list_chunks= list_chunks
        self._vocab = build_vocabulary(self._list_chunks)
        self._word_to_index={
            mot : index for index,mot in enumerate(self._vocab)
        }

        Nb_chunks = len(list_chunks)
        taille_vocab = len(self._vocab)

        self._chunk_matrix = np.zeros((Nb_chunks,taille_vocab))

        for i in range(Nb_chunks):
            self._chunk_matrix[i,:] = TF(self._word_to_index,list_chunks[i].content)

    @property
    def list_chunks(self):
        return self._list_chunks
    
    @property
    def vocab(self):
        return self._vocab
    
    @property
    def word_to_index(self):
        return self._word_to_index
    
    @property
    def chunk_matrix(self):
        return self._chunk_matrix
    
    def search(self,querry:str,k=3) -> list[tuple[float,Chunk]]:
        """
        fonction qui recherche grace a une querry dans le texte

        k doit etre inférieur ou égale a nombre de chunk.
        """
        if querry.strip() == "":
            raise ValueError("La requête ne peut pas être vide")

        k = min(k,len(self._list_chunks))
        vector_querry = TF(self._word_to_index,querry)
        scores = []
        for i in range(len(self._list_chunks)):
            vect1 = self._chunk_matrix[i,:]
            scores.append((cosine_similarity(vect1,vector_querry),self._list_chunks[i]))

        scores.sort(key=lambda x:x[0],reverse=True)

        return scores[:k]




if __name__=="__main__":
    from src.documents.read_txt import read_txt_file
    from src.documents.build_chunks import build_chunks

    FILEPATH = "/home/ielassad/smart-doc-search/data/raw/example.txt"
    source ="example"
    chunk_texts = read_txt_file(FILEPATH)
    chunk_list = build_chunks(chunk_texts,source)

    Engine = Engine(chunk_list) 

    def print_dict(dict):
        for key in dict.keys():
            print(f"Score : {key}\nChunk : [{dict[key]}]\n")
    res = Engine.search("loi Beer",3)
    # print(f" ========== Word index ==========\n{Engine.chunk_matrix}")
    # print(f"======= Score,Chunks =======\n{print_dict(res)}")
    print(res)
        
