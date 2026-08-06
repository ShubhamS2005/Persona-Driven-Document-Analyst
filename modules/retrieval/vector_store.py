import faiss
import numpy as np
import pickle
import os



class VectorStore:


    def __init__(
        self,
        path="data/vector_store"
    ):

        self.path = path

        self.index_path = os.path.join(
            self.path,
            "faiss.index"
        )

        self.embeddings_path = os.path.join(
            self.path,
            "embeddings.npy"
        )

        self.chunks_path = os.path.join(
            self.path,
            "chunks.pkl"
        )


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
            self.index_path
        )


        np.save(
            self.embeddings_path,
            embeddings
        )


        with open(
            self.chunks_path,
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


        print(
            "Loading FAISS index..."
        )


        index = faiss.read_index(
            self.index_path
        )


        print(
            "Loading embeddings..."
        )


        embeddings = np.load(
            self.embeddings_path
        )



        print(
            "Loading chunks..."
        )


        with open(
            self.chunks_path,
            "rb"
        ) as f:

            chunks = pickle.load(f)



        print(
            "Loaded:",
            index.ntotal,
            "vectors and",
            len(chunks),
            "chunks"
        )


        return (
            index,
            embeddings,
            chunks
        )