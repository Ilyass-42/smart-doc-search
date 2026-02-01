"""
Module Chunk.py
"""

class Chunk:
    def __init__(self,chunk_id: str,content: str, source: str,ordre: int):
        self._id = chunk_id
        self._content = content
        self._source = source
        self._ordre = ordre
    @property
    def id(self)-> str:
        return self._id
    @property
    def content(self) -> str:
        return self._content
    @property
    def source(self) -> str:
        return self._source
    @property
    def ordre(self)-> int:
        return self._ordre
    def __str__(self):
        return (
            f"Chunk ID : {self.id}, "
            f"Chunk source : {self.source}, "
            f"Chunk ordre : {self.ordre}\n"
        )
    def __repr__(self):
        return (
            f"Chunk ID : {self.id} "
            f"Chunk source : {self.source} "
            f"Chunk ordre : {self.ordre}\n"
        )
    

if __name__=="__main__":
    chunk_id_test ="PWM05"
    content_test ="PWM est Pulse Width Modulation"
    source_test ="PWM.txt"
    ordre_test=5

    chunk_test = Chunk(chunk_id_test,content_test,source_test,ordre_test)
    print(chunk_test)
