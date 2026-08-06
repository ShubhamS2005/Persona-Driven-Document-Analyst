import faiss
import numpy as np

class FAISSVectorStore:


    def __init__(self, dimension):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(
            dimension
        )


    def add_embeddings(
        self,
        embeddings
    ):

        if embeddings.dtype != np.float32:
            embeddings = embeddings.astype(
                "float32"
            )


        self.index.add(
            embeddings
        )


    def search(
        self,
        query_embedding,
        top_k=5
    ):

        if query_embedding.dtype != np.float32:
            query_embedding = query_embedding.astype(
                "float32"
            )


        scores, indices = self.index.search(
            query_embedding,
            top_k
        )


        return scores, indices



    def save(
        self,
        path
    ):

        faiss.write_index(
            self.index,
            path
        )


    def load(
        self,
        path
    ):

        self.index = faiss.read_index(
            path
        )