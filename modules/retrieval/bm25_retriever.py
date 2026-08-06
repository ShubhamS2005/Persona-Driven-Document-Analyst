from rank_bm25 import BM25Okapi
import json
import re



class BM25Retriever:


    def __init__(
        self,
        chunks_path="data/processed/processed_chunks.json"
    ):

        with open(
            chunks_path,
            encoding="utf-8"
        ) as f:

            self.chunks=json.load(f)



        self.documents=[

            chunk["text"]

            for chunk in self.chunks

        ]


        tokenized_docs=[

            self.tokenize(doc)

            for doc in self.documents

        ]


        self.bm25=BM25Okapi(
            tokenized_docs
        )



    def tokenize(
        self,
        text
    ):

        return re.findall(
            r"\w+",
            text.lower()
        )



    def retrieve(
        self,
        query,
        k=5
    ):


        tokens=self.tokenize(
            query
        )


        scores=self.bm25.get_scores(
            tokens
        )


        ranked_indexes=sorted(
            range(len(scores)),
            key=lambda i:scores[i],
            reverse=True
        )[:k]



        results=[]


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
                    float(scores[idx])

            })


        return results