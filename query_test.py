import pickle


from modules.retriever import Retriever



INDEX_PATH = (
    "data/vector_store/faiss.index"
)


CHUNKS_PATH = (
    "data/vector_store/chunks.pkl"
)



def load_chunks():

    with open(
        CHUNKS_PATH,
        "rb"
    ) as f:

        return pickle.load(f)



def main():

    chunks = load_chunks()


    retriever = Retriever(
        INDEX_PATH,
        chunks
    )


    query = (
        "Plan a 4 day trip for "
        "10 college friends"
    )


    results = retriever.search(
    query,
    retrieve_k=20,
    final_k=8
)


    print("\nTop Results\n")


    for i,result in enumerate(results):

        print("="*60)

        print(
            "Rank:",
            i+1
        )

        print(
    f"FAISS Score: {result.get('faiss_score',0):.4f}"
)

        print(
            f"Rerank Score: {result.get('rerank_score',0):.4f}"
        )


        print(
            "Document:",
            result["metadata"]["document"]
        )


        print(
            "Section:",
            result["metadata"]["section"]
        )


        print(
            "Page:",
            result["metadata"]["page"]
        )


        print(
            "\nText:"
        )


        print(
            result["text"][:300]
        )



if __name__=="__main__":
    main()