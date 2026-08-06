import json

from modules.retrieval.hybrid_retriever import HybridRetriever
from modules.retrieval.cross_encoder import CrossEncoderReranker



DATASET = ("data/evaluation/retrieval_dataset.json")

TOP_K = 5


def load_dataset():

    with open(DATASET,"r",encoding="utf-8") as f:

        return json.load(f)




def keyword_match(text,keywords):
    text = text.lower()
    matched = 0

    for word in keywords:
        if word.lower() in text:
            matched += 1



    return matched / len(keywords)




def evaluate():



    print(
        "\nLoading retriever..."
    )


    hybrid = HybridRetriever()


    reranker = CrossEncoderReranker()



    data = load_dataset()



    hybrid_hits = 0

    reranker_hits = 0


    total_keyword_score = 0



    for item in data:



        query = item["query"]


        expected = item[
            "expected_keywords"
        ]



        print(
            "\nQUERY:",
            query
        )



        results = hybrid.retrieve(

            query,

            top_k=20

        )



        # Hybrid evaluation


        top_text = "\n".join(

            [
                r["text"]

                for r in results[:TOP_K]
            ]

        )



        score = keyword_match(

            top_text,

            expected

        )



        total_keyword_score += score



        if score > 0:

            hybrid_hits +=1




        # Reranker evaluation


        reranked = reranker.rerank(

            query,

            results,

            top_k=TOP_K

        )



        rerank_text = "\n".join(

            [
                r["text"]

                for r in reranked
            ]

        )



        score = keyword_match(

            rerank_text,

            expected

        )



        if score > 0:

            reranker_hits +=1



        print(

            "Keyword Coverage:",

            round(score,2)

        )




    total=len(data)



    print("\n")
    print("="*60)
    print("BASELINE RESULTS")
    print("="*60)



    print(

        "Hybrid Recall@5:",

        round(
            hybrid_hits/total,
            3
        )

    )


    print(

        "Hybrid + Reranker Recall@5:",

        round(
            reranker_hits/total,
            3
        )

    )


    print(

        "Average Keyword Coverage:",

        round(
            total_keyword_score/total,
            3
        )

    )





if __name__=="__main__":


    evaluate()