import faiss
import numpy as np
import pickle
import os



class VectorStore:



    def __init__(
        self,
        path="data/vector_store"
    ):

        self.path=path

        os.makedirs(
            self.path,
            exist_ok=True
        )



    def create_index(
        self,
        embeddings
    ):


        dimension = embeddings.shape[1]


        index = faiss.IndexFlatIP(
            dimension
        )


        index.add(
            embeddings
        )


        print(
            "FAISS vectors:",
            index.ntotal
        )


        return index




    def save(
        self,
        index,
        embeddings,
        chunks
    ):


        faiss.write_index(
            index,
            f"{self.path}/faiss.index"
        )


        np.save(
            f"{self.path}/embeddings.npy",
            embeddings
        )


        with open(
            f"{self.path}/chunks.pkl",
            "wb"
        ) as f:

            pickle.dump(
                chunks,
                f
            )


        print(
            "Vector store saved"
        )




    def load(self):


        index = faiss.read_index(
            f"{self.path}/faiss.index"
        )


        with open(
            f"{self.path}/chunks.pkl",
            "rb"
        ) as f:

            chunks=pickle.load(f)


        return index,chunks