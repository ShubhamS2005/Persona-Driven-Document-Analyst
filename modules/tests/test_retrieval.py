from modules.retrieval.retriever import Retriever



def test_retrieval():


    retriever = Retriever()


    query = (
        "What are the historical sites "
        "in Carcassonne?"
    )


    results = retriever.search(
        query,
        top_k=3
    )



    print("\n\nQUERY:")
    print(query)



    print("\nTOP RESULTS:")



    for i,result in enumerate(results):


        print("\n----------------")

        print(
            "Rank:",
            i+1
        )

        print(
            "Score:",
            result["score"]
        )


        print(
            "Document:",
            result["metadata"]["document"]
        )


        print(
            "Section:",
            result["metadata"]["section_title"]
        )


        print(
            "Text:"
        )

        print(
            result["text"][:300]
        )




if __name__=="__main__":

    test_retrieval()