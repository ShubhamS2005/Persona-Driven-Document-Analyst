from modules.retrieval.retriever import Retriever
from modules.retrieval.context_builder import ContextBuilder



def test_context_builder():


    retriever = Retriever()



    query = (
        "What are the historical "
        "sites in Carcassonne?"
    )



    results = retriever.search(
        query,
        top_k=3
    )



    builder = ContextBuilder()



    context = builder.build(
        results
    )



    print("\nFINAL CONTEXT\n")

    print(
        context
    )



if __name__=="__main__":

    test_context_builder()