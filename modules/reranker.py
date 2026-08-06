from sentence_transformers import CrossEncoder


class CrossEncoderReranker:


    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )


    def rerank(
        self,
        query,
        documents
    ):


        pairs=[]


        for doc in documents:

            pairs.append(
                [
                    query,
                    doc["text"]
                ]
            )



        scores = self.model.predict(
            pairs
        )



        for doc,score in zip(
            documents,
            scores
        ):

            doc["rerank_score"]=float(score)



        documents.sort(
            key=lambda x:x["rerank_score"],
            reverse=True
        )


        return documents