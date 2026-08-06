import os
import numpy as np


from modules.vector_store import FAISSVectorStore



EMBEDDING_PATH = (
    "data/vector_store/embeddings.npy"
)


INDEX_PATH = (
    "data/vector_store/faiss.index"
)



def main():

    print(
        "Loading embeddings..."
    )


    embeddings = np.load(
        EMBEDDING_PATH
    )


    print(
        "Embedding shape:",
        embeddings.shape
    )


    dimension = embeddings.shape[1]


    print(
        "Creating FAISS index..."
    )


    vector_store = FAISSVectorStore(
        dimension
    )


    vector_store.add_embeddings(
        embeddings
    )


    print(
        "Total vectors:",
        vector_store.index.ntotal
    )


    os.makedirs(
        os.path.dirname(INDEX_PATH),
        exist_ok=True
    )


    vector_store.save(
        INDEX_PATH
    )


    print(
        "FAISS index saved:"
    )

    print(
        INDEX_PATH
    )



if __name__ == "__main__":
    main()