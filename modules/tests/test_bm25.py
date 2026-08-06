# from modules.retrieval.bm25_retriever import BM25Retriever



# retriever = BM25Retriever()



# query = "Cité de Carcassonne 52 towers"



# results = retriever.retrieve(
#     query,
#     k=3
# )



# for r in results:

#     print("\nSCORE:",
#           r["score"])

#     print(
#         r["text"][:300]
#     )

# from modules.retrieval.dense_retriever import DenseRetriever



# retriever=DenseRetriever()


# results=retriever.retrieve(
#     "Cité de Carcassonne 52 towers",
#     top_k=3
# )


# for r in results:

#     print("\n----")

#     print(
#         r["score"]
#     )

#     print(
#         r["text"][:300]
#     )

from modules.retrieval.hybrid_retriever import HybridRetriever


print("\nInitializing Hybrid Retriever...\n")


retriever = HybridRetriever()



query = "Suggest historical places for a tourist visiting South France"



print("QUERY:")
print(query)



results = retriever.retrieve(
    query,
    top_k=5
)



print("\n\nHYBRID RESULTS")
print("="*60)



for i,result in enumerate(results, start=1):

    print("\nRESULT:", i)

    print(
        "Hybrid Score:",
        result["score"]
    )


    print(
        "Dense Score:",
        result["dense_score"]
    )


    print(
        "BM25 Score:",
        result["bm25_score"]
    )


    print(
        "\nTEXT:"
    )

    print(
        result["text"][:500]
    )

    print("-"*60)