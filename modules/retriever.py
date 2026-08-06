from modules.embeddings import EmbeddingModel
from modules.vector_store import FAISSVectorStore
from modules.reranker import CrossEncoderReranker


class Retriever:

    def __init__(
        self,
        index_path,
        chunks,
        dimension=384
    ):

        print("Initializing retriever...")


        self.chunks = chunks


        print("Loading embedding model...")
        self.embedding_model = EmbeddingModel()


        print("Loading reranker...")
        self.reranker = CrossEncoderReranker()


        print("Loading FAISS index...")
        self.vector_store = FAISSVectorStore(
            dimension
        )

        self.vector_store.load(
            index_path
        )


        print("Retriever ready")


    def search(
        self,
        query,
        retrieve_k=20,
        final_k=5
    ):


        # --------------------------
        # 1. Encode query
        # --------------------------

        query_embedding = (
            self.embedding_model
            .encode_query(query)
        )


        # --------------------------
        # 2. Dense retrieval
        # --------------------------

        distances, indices = (
            self.vector_store.search(
                query_embedding,
                retrieve_k
            )
        )


        candidates=[]


        for idx,score in zip(
            indices[0],
            distances[0]
        ):


            if idx==-1:
                continue


            chunk=self.chunks[idx]


            candidates.append(
                {
                    "text":
                    chunk["text"],


                    "metadata":
                    chunk["metadata"],


                    "faiss_score":
                    float(score)
                }
            )



        print(
            f"FAISS candidates: {len(candidates)}"
        )



        # --------------------------
        # 3. Cross Encoder reranking
        # --------------------------

        reranked = (
            self.reranker
            .rerank(
                query,
                candidates
            )
        )


        return reranked[:final_k]