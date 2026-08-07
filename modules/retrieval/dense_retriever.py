import numpy as np

from modules.embedding.embedding_generator import EmbeddingGenerator
from modules.retrieval.vector_store import VectorStore



class DenseRetriever:


    def __init__(self):

        self.embedding_generator = EmbeddingGenerator()

        self.vector_store = VectorStore()

        self.index = None
        self.embeddings = None
        self.chunks = []

        self.load_store()



    # --------------------------------
    # LOAD VECTOR STORE
    # --------------------------------

    def load_store(self):

        (
            self.index,
            self.embeddings,
            self.chunks

        ) = self.vector_store.load()



        if self.index is None:

            print(
                "Dense Retriever: empty store"
            )

            self.chunks = []



    # --------------------------------
    # REFRESH AFTER UPLOAD / DELETE
    # --------------------------------

    def refresh(self):

        print(
            "Refreshing Dense Retriever..."
        )


        self.load_store()


        



    # --------------------------------
    # SEARCH
    # --------------------------------

    def retrieve(
        self,
        query,
        top_k=5
    ):


        # No documents yet

        if self.index is None:

            print(
                "No vectors available"
            )

            return []



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



        results = []



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