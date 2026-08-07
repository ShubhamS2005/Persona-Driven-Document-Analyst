import numpy as np

from modules.embedding.embedding_generator import EmbeddingGenerator
from modules.retrieval.vector_store import VectorStore



class DenseRetriever:


    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore()

        self.load_store()



    def load_store(self):

        (
            self.index,
            self.embeddings,
            self.chunks

        ) = self.vector_store.load()



    def refresh(self):

        print("Refreshing Dense Retriever...")

        self.load_store()

        print(
            "Dense Retriever refreshed:",
            len(self.chunks),
            "chunks"
        )



    # --------------------------------
    # Search
    # --------------------------------

    def retrieve(
        self,
        query,
        top_k=5
    ):


        query_embedding = (
            self.embedding_generator
            .generate_embeddings(
                [query]
            )
        )


        query_embedding = np.array(
            query_embedding
        ).astype(
            "float32"
        )


        scores, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )


        results=[]


        for score, idx in zip(
            scores[0],
            indices[0]
        ):


            if idx == -1:
                continue



            chunk = self.chunks[idx]


            results.append(

                {

                "text":
                chunk["text"],


                "metadata":
                chunk.get(
                    "metadata",
                    {}
                ),


                "score":
                float(score),


                "retriever":
                "dense"

                }

            )


        return results