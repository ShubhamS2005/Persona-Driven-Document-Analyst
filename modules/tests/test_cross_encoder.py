from modules.retrieval.hybrid_retriever import HybridRetriever
from modules.retrieval.cross_encoder import CrossEncoderReranker



query = (
    "Suggest historical places "
    "for a tourist visiting South France"
)



print("\nLoading Hybrid Retriever...\n")


hybrid = HybridRetriever()



results = hybrid.retrieve(
    query,
    top_k=30
)



print("\nBEFORE RERANKING")
print("="*60)



for i,r in enumerate(
    results[:5],
    start=1
):

    print("\n",i)

    print(
        r["score"]
    )

    print(
        r["text"][:200]
    )



print("\n\nLoading Cross Encoder...\n")



reranker = CrossEncoderReranker()



reranked = reranker.rerank(

    query,

    results,

    top_k=5

)



print("\nAFTER RERANKING")
print("="*60)



for i,r in enumerate(
    reranked,
    start=1
):


    print("\nRESULT:",i)


    print(
        "Rerank Score:",
        r["score"]
    )


    print(
        "Old Hybrid:",
        r["previous_score"]
    )


    print(
        r["text"][:400]
    )