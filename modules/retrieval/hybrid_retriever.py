import re

from rank_bm25 import BM25Okapi

from modules.retrieval.dense_retriever import DenseRetriever



class HybridRetriever:


    def __init__(self):


        self.dense = DenseRetriever()


        self.documents = []


        self.bm25 = None


        self.build_bm25()



    # --------------------------------
    # TOKENIZER
    # --------------------------------

    def _tokenize(self, text):

        return re.findall(
            r"\b[a-z]{3,}\b",
            text.lower()
        )



    # --------------------------------
    # BUILD BM25 SAFELY
    # --------------------------------

    def build_bm25(self):


        self.documents = self.dense.chunks



        if not self.documents:


            print(
                "Hybrid Retriever: empty store"
            )


            self.bm25 = None


            return



        tokenized = [

            self._tokenize(
                doc["text"]
            )

            for doc in self.documents

        ]



        self.bm25 = BM25Okapi(
            tokenized
        )


        



    # --------------------------------
    # NORMALIZE
    # --------------------------------

    def _normalize(self, scores):


        scores = list(scores)


        if not scores:

            return []



        min_score = min(scores)

        max_score = max(scores)



        if max_score == min_score:

            return [

                0.0

                for _ in scores

            ]



        return [

            float(
                (score-min_score)
                /
                (max_score-min_score)
            )

            for score in scores

        ]



    # --------------------------------
    # RETRIEVE
    # --------------------------------

    def retrieve(
        self,
        query,
        top_k=5,
        alpha=0.7
    ):


        if not self.documents:

            print(
                "No documents available"
            )

            return []



        # -----------------------------
        # Dense retrieval
        # -----------------------------


        dense_results = self.dense.retrieve(

            query,

            top_k=len(self.documents)

        )



        dense_score_map = {

            result["text"]:
            result["score"]

            for result in dense_results

        }



        dense_scores = [

            dense_score_map.get(

                doc["text"],

                0

            )

            for doc in self.documents

        ]



        # -----------------------------
        # BM25 retrieval
        # -----------------------------


        if self.bm25 is not None:


            query_tokens = self._tokenize(
                query
            )


            bm25_scores = self.bm25.get_scores(
                query_tokens
            )


        else:


            bm25_scores = [

                0

                for _ in self.documents

            ]



        # -----------------------------
        # Normalize
        # -----------------------------


        dense_norm = self._normalize(
            dense_scores
        )


        bm25_norm = self._normalize(
            bm25_scores
        )



        # -----------------------------
        # Fusion
        # -----------------------------


        results=[]



        for idx,doc in enumerate(
            self.documents
        ):


            score = (

                alpha *
                dense_norm[idx]

                +

                (1-alpha)
                *
                bm25_norm[idx]

            )



            results.append({


                "text":

                doc["text"],



                "metadata":

                doc.get(
                    "metadata",
                    {}
                ),



                "score":

                float(score),



                "dense_score":

                float(
                    dense_scores[idx]
                ),



                "bm25_score":

                float(
                    bm25_scores[idx]
                ),



                "retriever":

                "hybrid"


            })



        results.sort(

            key=lambda x:x["score"],

            reverse=True

        )


        return results[:top_k]



    # --------------------------------
    # REFRESH AFTER UPLOAD / DELETE
    # --------------------------------

    def refresh(self):


        print(
            "Refreshing Hybrid Retriever..."
        )



        self.dense.refresh()



        self.build_bm25()



        print(
            "Hybrid Retriever refreshed:",
            len(self.documents),
        )