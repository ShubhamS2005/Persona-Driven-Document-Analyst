from sentence_transformers import CrossEncoder



class CrossEncoderReranker:
    def __init__(self,model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        print("Loading Cross Encoder...")
        self.model = CrossEncoder(
            model_name
        )

    def rerank(self,query,documents,top_k=5):
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



        results=[]


        for doc,score in zip(documents,scores):
            results.append(
                {
                    "text":
                    doc["text"],

                    "score":
                    float(score),

                    "previous_score":
                    doc.get(
                        "score",
                        0
                    ),

                    "retriever":
                    "cross_encoder"

                }

            )



        results.sort(
            key=lambda x:x["score"],
            reverse=True
        )



        return results[:top_k]