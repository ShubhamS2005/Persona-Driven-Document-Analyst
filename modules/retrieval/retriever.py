import os
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer



class Retriever:


    def __init__(
        self,
        vector_path="data/vector_store/faiss.index",
        chunks_path="data/vector_store/chunks.pkl",
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):


        print("Loading embedding model...")

        self.model = SentenceTransformer(
            model_name
        )


        print("Loading FAISS index...")


        self.index = faiss.read_index(
            vector_path
        )


        print(
            "Vectors loaded:",
            self.index.ntotal
        )


        with open(
            chunks_path,
            "rb"
        ) as f:

            self.chunks = pickle.load(
                f
            )


        print(
            "Chunks loaded:",
            len(self.chunks)
        )



    def embed_query(
        self,
        query
    ):


        embedding = self.model.encode(
            [query],
            normalize_embeddings=True
        )


        return np.array(
            embedding
        ).astype(
            "float32"
        )



    def search(
        self,
        query,
        top_k=5
    ):


        query_vector = self.embed_query(
            query
        )


        scores, indices = self.index.search(
            query_vector,
            top_k
        )


        results=[]



        for score,index in zip(
            scores[0],
            indices[0]
        ):


            if index == -1:
                continue



            chunk=self.chunks[index]


            results.append({

                "score":float(score),

                "text":
                chunk["text"],

                "metadata":
                chunk["metadata"]

            })


        return results