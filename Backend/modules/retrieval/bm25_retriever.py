from rank_bm25 import BM25Okapi
import re

from modules.retrieval.vector_store import VectorStore



class BM25Retriever:


    def __init__(self):


        self.vector_store = VectorStore()

        self.chunks = []

        self.bm25 = None


        self.load_store()



    # --------------------------------
    # LOAD CHUNKS FROM VECTOR STORE
    # --------------------------------

    def load_store(self):


        (
            _,
            _,
            self.chunks

        ) = self.vector_store.load()



        if not self.chunks:

            print(
                "BM25 Retriever: empty store"
            )

            self.bm25 = None

            return



        documents = [

            chunk["text"]

            for chunk in self.chunks

        ]



        tokenized_docs = [

            self.tokenize(doc)

            for doc in documents

        ]



        self.bm25 = BM25Okapi(
            tokenized_docs
        )


        print(
            "BM25 loaded:",
            len(self.chunks),
            "chunks"
        )



    # --------------------------------
    # REFRESH AFTER UPLOAD / DELETE
    # --------------------------------

    def refresh(self):


        print(
            "Refreshing BM25..."
        )


        self.load_store()



    # --------------------------------
    # TOKENIZER
    # --------------------------------

    def tokenize(
        self,
        text
    ):


        return re.findall(
            r"\w+",
            text.lower()
        )



    # --------------------------------
    # SEARCH
    # --------------------------------

    def retrieve(
        self,
        query,
        k=5
    ):


        if self.bm25 is None:

            return []



        tokens = self.tokenize(
            query
        )


        scores = self.bm25.get_scores(
            tokens
        )



        ranked_indexes = sorted(

            range(len(scores)),

            key=lambda i: scores[i],

            reverse=True

        )[:k]



        results = []



        for idx in ranked_indexes:


            results.append({

                "text":
                self.chunks[idx]["text"],


                "metadata":
                self.chunks[idx].get(
                    "metadata",
                    {}
                ),


                "score":
                float(scores[idx]),


                "retriever":
                "bm25"

            })



        return results