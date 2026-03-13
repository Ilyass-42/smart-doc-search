from src.documents.chunk_model import Chunk
from src.preprocessing.vectorizer import build_vocabulary
from src.preprocessing.vectorizer import TF
from src.preprocessing.vectorizer import cosine_similarity
from src.preprocessing.vectorizer import normalize
from src.preprocessing.vectorizer import normalize_vector
import hashlib

import numpy as np


class Engine:
    def __init__(self,list_chunks:list[Chunk]):
        self._list_chunks= list_chunks
        self._files_hashes = set()
        self._vocab = build_vocabulary(self._list_chunks)
        self._idf_vector = np.array([])
        self._word_to_index={
            mot : index for index,mot in enumerate(self._vocab)
        }

        Nb_chunks = len(list_chunks)
        taille_vocab = len(self._vocab)

        self._chunk_matrix = np.zeros((Nb_chunks,taille_vocab))

        for i in range(Nb_chunks):
            self._chunk_matrix[i,:] = TF(self._word_to_index,list_chunks[i].content)
        if list_chunks:
            self._idf_vector = self._compute_idf()
            self._chunk_matrix = self._chunk_matrix*self._idf_vector


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
    
    def add(self,chunks: list[Chunk]):
        new_chunks = []

        for c in chunks:
            content_hash = hashlib.sha256(c.content.encode()).hexdigest()

            if (c.source,content_hash) not in self._files_hashes:
                self._files_hashes.add((c.source,content_hash))
                new_chunks.append(c)
            

        if new_chunks:
            self._list_chunks.extend(new_chunks)
            new_vocab = build_vocabulary(new_chunks)

            taille_vocab_old = len(self._vocab)

            new_mots = [mot for mot in new_vocab if mot not in self._vocab]
            
            for mot in new_mots:
                self._vocab.append(mot)
            
            taille_vocab_new = len(self._vocab)
                

            indice_depart = len(self._word_to_index)
            
            self._word_to_index.update(
                {mot:index+indice_depart for index,mot in enumerate(new_mots)})
            
            new_vectors = np.array([TF(self._word_to_index, c.content) for c in new_chunks])
            
            valeur_padding = taille_vocab_new-taille_vocab_old
            if self._chunk_matrix.size == 0:
                self._chunk_matrix = new_vectors

            else:
                self._chunk_matrix = np.pad(self._chunk_matrix,((0,0),(0,valeur_padding)),mode = 'constant',constant_values=0)
                self._chunk_matrix = np.vstack([self._chunk_matrix, new_vectors])
                
            self._idf_vector = self._compute_idf()
            self._chunk_matrix = self._chunk_matrix*self._idf_vector




    def _compute_idf(self)->list[float]:
        if  len(self._list_chunks)==0:
            raise ValueError("Aucun chunk dans l'engine")
        self._idf_vector = []
        N = len(self._list_chunks)

        tokenized = [set(normalize(c.content))for c in self._list_chunks]

        for mot in self._vocab:
            df = sum(1 for tokens in tokenized if mot in tokens)
            df = max(df,1)
            self._idf_vector.append(np.log(N/df))

        self._idf_vector = np.array(self._idf_vector)
        return self._idf_vector

    
        
    
    def search(self,querry:str,k=3) -> list[tuple[float,Chunk]]:
        """
        fonction qui recherche grace a une querry dans le texte

        k doit etre inférieur ou égale a nombre de chunk.
        """
        if querry.strip() == "":
            raise ValueError("La requête ne peut pas être vide")
        if  self._idf_vector.size<=0:
            raise ValueError("Len = 0")
        k = min(k,len(self._list_chunks))
        
        vector_querry = normalize_vector(TF(self._word_to_index,querry)*self._idf_vector)
        if len(self._list_chunks) == 0:
            raise ValueError("Il y a pas de chunk")

        norms = np.linalg.norm(self.chunk_matrix,axis=1,keepdims=True)
        norms[norms == 0] = 1        
        normalized_matrix = self._chunk_matrix / norms

        scores = normalized_matrix @ vector_querry
        top_k = np.argsort(scores)[::-1][:k]

        return [(scores[i], self._list_chunks[i]) for i in top_k]



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
        
