import re

from rank_bm25 import BM25Okapi

from modules.retrieval.dense_retriever import DenseRetriever



class HybridRetriever:


    def __init__(self):


        self.dense = DenseRetriever()


        self.documents = self.dense.chunks



        tokenized = [

            self._tokenize(
                doc["text"]
            )

            for doc in self.documents

        ]


        self.bm25 = BM25Okapi(
            tokenized
        )



    def _tokenize(self, text):

        return re.findall(
            r"\b[a-z]{3,}\b",
            text.lower()
        )



    def _normalize(self, scores):


        scores = list(scores)


        if len(scores) == 0:
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



    def retrieve(
        self,
        query,
        top_k=5,
        alpha=0.7
    ):


        # =========================
        # Dense Retrieval
        # =========================


        dense_results = self.dense.retrieve(
            query,
            top_k=len(self.documents)
        )


        dense_score_map = {}


        for result in dense_results:


            dense_score_map[
                result["text"]
            ] = result["score"]




        dense_scores = [

            dense_score_map.get(
                doc["text"],
                0
            )

            for doc in self.documents

        ]



        # =========================
        # BM25 Retrieval
        # =========================


        query_tokens = self._tokenize(
            query
        )


        bm25_scores = self.bm25.get_scores(
            query_tokens
        )



        # =========================
        # Normalize
        # =========================


        dense_scores_norm = self._normalize(
            dense_scores
        )


        bm25_scores_norm = self._normalize(
            bm25_scores
        )



        # =========================
        # Fusion
        # =========================


        results=[]


        for idx,doc in enumerate(
            self.documents
        ):


            hybrid_score = (

                alpha *
                dense_scores_norm[idx]

                +

                (1-alpha)
                *
                bm25_scores_norm[idx]

            )



            results.append(

                {

                "text":
                doc["text"],


                "metadata":
                doc.get(
                    "metadata",
                    {}
                ),


                "score":
                float(
                    hybrid_score
                ),


                "dense_score":
                float(
                    dense_scores[idx]
                ),


                "bm25_score":
                float(
                    bm25_scores[idx]
                ),


                "dense_normalized":
                float(
                    dense_scores_norm[idx]
                ),


                "bm25_normalized":
                float(
                    bm25_scores_norm[idx]
                ),


                "retriever":
                "hybrid"

                }

            )



        results.sort(

            key=lambda x:x["score"],

            reverse=True

        )


        return results[:top_k]